# TempAI Architecture - Local & Free RAG System

## Overview

TempAI is a fully local, open-source RAG (Retrieval-Augmented Generation) chatbot for answering questions about YouTube videos. Everything runs on your machine - no API calls, no cloud services, completely free.

## Technology Stack

### Core Components

| Component | Technology | Purpose | License |
|-----------|-----------|---------|---------|
| **LLM** | Ollama + Llama 3.2 | Answer generation | Apache 2.0 |
| **Embeddings** | sentence-transformers | Text→Vector conversion | Apache 2.0 |
| **Vector Database** | ChromaDB | Semantic search storage | Apache 2.0 |
| **RAG Framework** | LangChain | Orchestration | MIT |
| **Video Extraction** | yt-dlp | Transcript extraction | Unlicense |
| **Web UI** | Streamlit | User interface | Apache 2.0 |
| **Language** | Python 3.9+ | Runtime | PSF |

### Why These Choices?

**Ollama vs Cloud APIs (GPT-4, Claude)**
- ✅ Completely free - no token costs
- ✅ No rate limits
- ✅ Privacy - data never leaves your machine
- ✅ Works offline
- ⚠️ Slightly slower inference (but acceptable)
- ⚠️ Requires ~4-8GB RAM per model

**ChromaDB vs Pinecone/Weaviate**
- ✅ Embedded - no separate server
- ✅ Zero configuration
- ✅ Persistent local storage
- ✅ Fast enough for single-user use
- Works well with up to millions of vectors

**sentence-transformers vs OpenAI Embeddings**
- ✅ Free and local
- ✅ Fast inference (~50ms per query)
- ✅ Decent quality (384 dimensions)
- Model: all-MiniLM-L6-v2 (80MB)

## System Architecture

### High-Level Flow

```
┌──────────────┐
│     User     │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         Streamlit Web Interface         │
│  - Video URL input                      │
│  - Question input                       │
│  - Answer display with sources          │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│        RAG Pipeline (LangChain)         │
│                                         │
│  Mode 1: Process Video                 │
│  Mode 2: Answer Questions              │
└─────────────────────────────────────────┘
       │
       ├─────────────────┬─────────────────┐
       ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   yt-dlp     │  │  ChromaDB    │  │   Ollama     │
│  (Extract)   │  │  (Search)    │  │  (Generate)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### Detailed Component Architecture

#### 1. Video Processing Pipeline

```python
YouTubeAnalyzer.get_transcript(url)
    ↓
Raw Transcript Text
    ↓
RecursiveCharacterTextSplitter
    - chunk_size: 500 tokens
    - chunk_overlap: 50 tokens
    - separators: ["\n\n", "\n", ". ", " "]
    ↓
Text Chunks with Metadata
    {
        "text": "chunk content",
        "video_id": "abc123",
        "video_title": "Example Video",
        "timestamp": "00:05:23",
        "chunk_index": 0
    }
    ↓
SentenceTransformer.encode()
    - Model: all-MiniLM-L6-v2
    - Output: 384-dimensional vector
    ↓
ChromaDB.add()
    - Collection per video
    - Metadata preserved
    - Automatic indexing
```

#### 2. Question Answering Pipeline

```python
User Question: "What did they say about X?"
    ↓
SentenceTransformer.encode(question)
    - Same model as documents
    - 384-dimensional query vector
    ↓
ChromaDB.query(query_vector, k=5)
    - Cosine similarity search
    - Returns top-5 most relevant chunks
    ↓
Context Builder
    - Sort by relevance score
    - Format with timestamps
    - Add video metadata
    ↓
Prompt Template
    """
    Context from video "{title}":

    [00:05:23] {chunk_1_text}
    [00:12:45] {chunk_2_text}
    ...

    Question: {user_question}

    Answer based only on the context above. Include timestamps.
    """
    ↓
Ollama.generate()
    - Model: llama3.2 or mistral
    - Temperature: 0.1 (factual)
    - Max tokens: 500
    ↓
Structured Response
    {
        "answer": "...",
        "sources": [
            {"timestamp": "00:05:23", "relevance": 0.89},
            {"timestamp": "00:12:45", "relevance": 0.82}
        ],
        "confidence": "high"
    }
    ↓
Display to User
```

## Data Storage

### Directory Structure

```
TempAI/
├── youtube_analyzer/          # Video extraction
│   └── youtube_analyzer.py
├── rag_chatbot/              # Main RAG implementation
│   ├── __init__.py
│   ├── video_processor.py    # Process videos → ChromaDB
│   ├── qa_engine.py          # Question answering logic
│   ├── embeddings.py         # Embedding management
│   └── prompts.py            # Prompt templates
├── data/                     # Local data storage
│   ├── chromadb/            # Vector database
│   │   └── chroma.sqlite3
│   └── videos/              # Video metadata cache
│       └── {video_id}.json
├── models/                   # Downloaded models
│   └── sentence-transformers/
│       └── all-MiniLM-L6-v2/
├── app.py                   # Streamlit interface
└── requirements.txt
```

### ChromaDB Schema

**Collection per video:**
- Collection name: `video_{youtube_id}`
- Embeddings: 384-dimensional vectors
- Metadata per document:
  ```json
  {
    "text": "actual chunk text",
    "video_id": "dQw4w9WgXcQ",
    "video_title": "Example Video Title",
    "channel": "Channel Name",
    "timestamp_seconds": 323,
    "timestamp_formatted": "00:05:23",
    "chunk_index": 5,
    "total_chunks": 150,
    "upload_date": "2024-01-15"
  }
  ```

## Performance Characteristics

### Speed Benchmarks (on modest hardware)

**Video Processing:**
- 10 min video → ~15-30 seconds to process
- Transcript extraction: ~5s
- Chunking: instant
- Embedding generation: ~10-20s (CPU)
- ChromaDB insertion: ~5s

**Question Answering:**
- Query embedding: ~50ms
- Vector search: ~100ms
- LLM generation: ~2-5s (depends on answer length)
- **Total: ~3-6 seconds per question**

### Resource Usage

**Disk Space:**
- Ollama models: 4-8GB per model
- sentence-transformers: 80MB
- ChromaDB: ~10MB per hour of video
- Total: ~10GB minimum

**Memory (RAM):**
- Baseline Python: 200MB
- sentence-transformers: 500MB
- ChromaDB: 100MB
- Ollama (Llama 3.2): 4-8GB
- **Total: 6-10GB recommended**

**CPU Usage:**
- Embedding: 50-100% (brief spikes)
- Vector search: <10%
- LLM inference: 100% (sustained during generation)

**GPU (Optional):**
- With CUDA: 3-5x faster embeddings
- With CUDA: 2-4x faster LLM inference
- Ollama automatically uses GPU if available

## Scalability Limits

### Single Video
- ✅ Works perfectly
- Response time: 3-6s

### Multiple Videos (2-10)
- ✅ Works well
- Separate collection per video
- Need to specify which video to query

### Many Videos (10-100)
- ⚠️ Need collection management
- Consider merging collections
- May need metadata filtering

### Large Scale (100+)
- ❌ Not recommended for this architecture
- Consider upgrading to Qdrant or Weaviate
- Or use cloud-based solution

## Security & Privacy

### Data Privacy
- ✅ All data stays local
- ✅ No telemetry
- ✅ No external API calls
- ✅ Can run completely offline (after initial setup)

### Sensitive Content
- Video transcripts stored locally in ChromaDB
- Clear storage: Delete `data/chromadb/` directory
- Per-video deletion: Drop specific collection

## Future Enhancements

### Near-term (Easy)
- [ ] Multi-video conversations
- [ ] Export chat history
- [ ] Dark mode UI
- [ ] Video player integration (show timestamp)

### Mid-term (Moderate)
- [ ] Multi-language support
- [ ] Summarization mode
- [ ] Batch video processing
- [ ] GPU acceleration toggle

### Long-term (Complex)
- [ ] Visual frame analysis (multimodal)
- [ ] Speaker diarization
- [ ] Auto-generated video summaries
- [ ] Mobile app

## Alternatives Considered

### Why not use cloud LLMs?
- Cost: Would need paid API (GPT-4: $0.03/1k tokens)
- Privacy: Video content sent to third parties
- Rate limits: Restricted usage
- **Decision: Ollama provides good enough quality for free**

### Why not fine-tune a model?
- Complexity: Requires training infrastructure
- Cost: GPU time for training
- Maintenance: Need to retrain for improvements
- **Decision: RAG is more flexible and easier**

### Why not use RAG-specific frameworks (LlamaIndex)?
- Both LangChain and LlamaIndex work
- LangChain has more examples/documentation
- Slightly more active community
- **Decision: Either works, LangChain chosen**

## References

- [Ollama Documentation](https://ollama.ai/docs)
- [ChromaDB Documentation](https://docs.trychroma.com)
- [LangChain Documentation](https://python.langchain.com)
- [sentence-transformers](https://www.sbert.net)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
