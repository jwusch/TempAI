"""Process YouTube videos and store in vector database"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings
import re

# Add youtube_analyzer to path
sys.path.append(str(Path(__file__).parent.parent / "youtube_analyzer"))
from youtube_analyzer import YouTubeAnalyzer

from .embeddings import EmbeddingModel


class VideoProcessor:
    """Processes YouTube videos and stores them in ChromaDB"""

    def __init__(
        self,
        persist_directory: str = "./data/chromadb",
        embedding_model_name: str = "all-MiniLM-L6-v2"
    ):
        """
        Initialize the video processor

        Args:
            persist_directory: Directory to persist ChromaDB data
            embedding_model_name: Name of the embedding model
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)

        # Initialize embedding model
        self.embedding_model = EmbeddingModel(embedding_model_name)

        # Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.persist_directory)
        )

        # Initialize YouTube analyzer
        self.youtube_analyzer = YouTubeAnalyzer()

    def _extract_video_id(self, url: str) -> str:
        """Extract YouTube video ID from URL"""
        # Handle various YouTube URL formats
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]*)',
            r'youtube\.com\/embed\/([^&\n?]*)',
            r'youtube\.com\/v\/([^&\n?]*)'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # If no pattern matches, assume it's already a video ID
        return url

    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> List[str]:
        """
        Split text into overlapping chunks

        Args:
            text: Text to chunk
            chunk_size: Approximate size of each chunk in characters
            chunk_overlap: Number of characters to overlap between chunks

        Returns:
            List of text chunks
        """
        if not text or len(text) == 0:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size

            # If this isn't the last chunk, try to break at a sentence
            if end < text_length:
                # Look for sentence endings
                for separator in ['. ', '.\n', '! ', '?\n', '? ']:
                    last_separator = text.rfind(separator, start, end)
                    if last_separator != -1:
                        end = last_separator + 1
                        break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - chunk_overlap if end < text_length else text_length

        return chunks

    def process_video(
        self,
        video_url: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> Dict:
        """
        Process a YouTube video and store in vector database

        Args:
            video_url: YouTube video URL
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks

        Returns:
            Dictionary with processing results
        """
        print(f"\n📹 Processing video: {video_url}")

        # Extract video ID
        video_id = self._extract_video_id(video_url)
        collection_name = f"video_{video_id}"

        # Check if video already processed
        try:
            existing_collection = self.chroma_client.get_collection(collection_name)
            if existing_collection.count() > 0:
                print(f"✅ Video already processed ({existing_collection.count()} chunks)")
                return {
                    "status": "already_exists",
                    "video_id": video_id,
                    "collection_name": collection_name,
                    "chunk_count": existing_collection.count()
                }
        except:
            pass  # Collection doesn't exist yet

        # Get video info
        print("📊 Extracting video metadata...")
        video_info = self.youtube_analyzer.get_video_info(video_url)

        if "error" in video_info:
            return {"status": "error", "error": video_info["error"]}

        # Get transcript
        print("📝 Extracting transcript...")
        transcript_info = self.youtube_analyzer.get_transcript(video_url)

        if "error" in transcript_info:
            return {"status": "error", "error": transcript_info["error"]}

        # For now, use description as a fallback if no transcript
        # In a real implementation, you'd extract the actual subtitles
        text_content = video_info.get("description", "")

        if not text_content or len(text_content) < 50:
            return {
                "status": "error",
                "error": "No transcript or description available for this video"
            }

        # Chunk the text
        print(f"✂️  Chunking text (size={chunk_size}, overlap={chunk_overlap})...")
        chunks = self._chunk_text(text_content, chunk_size, chunk_overlap)

        if not chunks:
            return {"status": "error", "error": "Failed to create chunks from video content"}

        print(f"📦 Created {len(chunks)} chunks")

        # Generate embeddings
        print("🧮 Generating embeddings...")
        embeddings = self.embedding_model.embed_batch(chunks)

        # Create or get collection
        collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            metadata={
                "video_id": video_id,
                "video_title": video_info.get("title", "Unknown"),
                "channel": video_info.get("channel", "Unknown")
            }
        )

        # Prepare documents and metadata
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "video_id": video_id,
                "video_title": video_info.get("title", "Unknown"),
                "channel": video_info.get("channel", "Unknown"),
                "chunk_index": i,
                "total_chunks": len(chunks),
                "upload_date": video_info.get("upload_date", "Unknown"),
                "video_url": video_url
            }
            for i in range(len(chunks))
        ]

        # Add to ChromaDB
        print("💾 Storing in vector database...")
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas
        )

        print(f"✅ Video processed successfully!")
        print(f"   Title: {video_info.get('title', 'Unknown')}")
        print(f"   Chunks: {len(chunks)}")
        print(f"   Collection: {collection_name}")

        return {
            "status": "success",
            "video_id": video_id,
            "collection_name": collection_name,
            "video_info": video_info,
            "chunk_count": len(chunks)
        }

    def list_processed_videos(self) -> List[Dict]:
        """List all processed videos"""
        collections = self.chroma_client.list_collections()
        videos = []

        for collection in collections:
            if collection.name.startswith("video_"):
                video_id = collection.name.replace("video_", "")
                metadata = collection.metadata or {}
                videos.append({
                    "video_id": video_id,
                    "collection_name": collection.name,
                    "title": metadata.get("video_title", "Unknown"),
                    "channel": metadata.get("channel", "Unknown"),
                    "chunk_count": collection.count()
                })

        return videos

    def delete_video(self, video_id: str) -> bool:
        """Delete a processed video from the database"""
        collection_name = f"video_{video_id}"
        try:
            self.chroma_client.delete_collection(collection_name)
            return True
        except:
            return False
