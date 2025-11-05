"""Question answering engine using RAG"""

from typing import Dict, List, Optional
import chromadb
from pathlib import Path

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("⚠️  Warning: ollama package not available. Install with: pip install ollama")

from .embeddings import EmbeddingModel
from .prompts import (
    QA_SYSTEM_PROMPT,
    QA_PROMPT_TEMPLATE,
    CONTEXT_CHUNK_TEMPLATE,
    NO_CONTEXT_RESPONSE
)


class QAEngine:
    """Handles question answering using RAG"""

    def __init__(
        self,
        persist_directory: str = "./data/chromadb",
        embedding_model_name: str = "all-MiniLM-L6-v2",
        llm_model: str = "llama3.2",
        top_k: int = 5
    ):
        """
        Initialize the QA engine

        Args:
            persist_directory: Directory where ChromaDB data is stored
            embedding_model_name: Name of the embedding model
            llm_model: Name of the Ollama model to use
            top_k: Number of relevant chunks to retrieve
        """
        self.persist_directory = Path(persist_directory)
        self.llm_model = llm_model
        self.top_k = top_k

        # Initialize embedding model
        self.embedding_model = EmbeddingModel(embedding_model_name)

        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

    def _check_ollama(self) -> bool:
        """Check if Ollama is available and running"""
        if not OLLAMA_AVAILABLE:
            return False

        try:
            ollama.list()
            return True
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return False

    def answer_question(
        self,
        question: str,
        video_id: str,
        temperature: float = 0.1,
        max_tokens: int = 500
    ) -> Dict:
        """
        Answer a question about a video

        Args:
            question: User's question
            video_id: YouTube video ID
            temperature: LLM temperature (lower = more factual)
            max_tokens: Maximum tokens in response

        Returns:
            Dictionary with answer and metadata
        """
        collection_name = f"video_{video_id}"

        # Get collection
        try:
            collection = self.chroma_client.get_collection(collection_name)
        except Exception as e:
            return {
                "status": "error",
                "error": f"Video not found. Please process the video first. ({e})"
            }

        # Get collection metadata
        collection_metadata = collection.metadata or {}
        video_title = collection_metadata.get("video_title", "Unknown")
        channel = collection_metadata.get("channel", "Unknown")

        # Embed the question
        print(f"🔍 Searching for relevant content...")
        question_embedding = self.embedding_model.embed_text(question)

        # Query ChromaDB for relevant chunks
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=min(self.top_k, collection.count())
        )

        if not results or not results['documents'] or len(results['documents'][0]) == 0:
            return {
                "status": "no_context",
                "answer": NO_CONTEXT_RESPONSE,
                "sources": []
            }

        # Build context from retrieved chunks
        chunks = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]

        context_parts = []
        sources = []

        for i, (chunk, metadata, distance) in enumerate(zip(chunks, metadatas, distances)):
            # Use chunk index as a proxy for timestamp
            chunk_idx = metadata.get('chunk_index', i)
            timestamp = f"Part {chunk_idx + 1}"

            context_parts.append(
                CONTEXT_CHUNK_TEMPLATE.format(
                    timestamp=timestamp,
                    text=chunk
                )
            )

            sources.append({
                "chunk_index": chunk_idx,
                "timestamp": timestamp,
                "text_preview": chunk[:100] + "..." if len(chunk) > 100 else chunk,
                "relevance_score": 1 - distance  # Convert distance to similarity
            })

        context = "\n\n".join(context_parts)

        # Build the prompt
        prompt = QA_PROMPT_TEMPLATE.format(
            video_title=video_title,
            channel=channel,
            context=context,
            question=question
        )

        # Check if Ollama is available
        if not self._check_ollama():
            # Fallback: return context without LLM generation
            return {
                "status": "no_llm",
                "answer": "⚠️ Ollama is not available. Here's the relevant context from the video:\n\n" + context,
                "sources": sources,
                "video_title": video_title,
                "video_id": video_id
            }

        # Generate answer using Ollama
        print(f"🤖 Generating answer with {self.llm_model}...")

        try:
            response = ollama.generate(
                model=self.llm_model,
                prompt=prompt,
                system=QA_SYSTEM_PROMPT,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens,
                }
            )

            answer = response.get('response', '').strip()

            return {
                "status": "success",
                "answer": answer,
                "sources": sources,
                "video_title": video_title,
                "video_id": video_id,
                "model_used": self.llm_model
            }

        except Exception as e:
            # Fallback to context if LLM fails
            return {
                "status": "llm_error",
                "answer": f"⚠️ Error generating answer: {e}\n\nRelevant context:\n\n{context}",
                "sources": sources,
                "video_title": video_title,
                "video_id": video_id,
                "error": str(e)
            }

    def list_available_videos(self) -> List[Dict]:
        """List all videos available for Q&A"""
        collections = self.chroma_client.list_collections()
        videos = []

        for collection in collections:
            if collection.name.startswith("video_"):
                video_id = collection.name.replace("video_", "")
                metadata = collection.metadata or {}
                videos.append({
                    "video_id": video_id,
                    "title": metadata.get("video_title", "Unknown"),
                    "channel": metadata.get("channel", "Unknown"),
                    "chunks": collection.count()
                })

        return videos
