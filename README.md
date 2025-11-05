# TempAI - Video Q&A RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that allows users to ask questions about YouTube videos. The system extracts video content (transcripts, metadata, captions) and uses RAG techniques to provide accurate, contextual answers based on the video content.

## Project Vision

TempAI enables users to:
- Input a YouTube video URL
- Ask natural language questions about the video content
- Receive accurate answers extracted from video transcripts and metadata
- Get timestamped references to relevant video sections

## Current Components

### YouTube Analyzer (✅ Implemented)
Located in `youtube_analyzer/` - A Python tool that:
- Extracts video metadata (title, description, views, etc.)
- Downloads video transcripts and captions
- Supports multiple languages
- Provides JSON output for integration

See [youtube_analyzer/README.md](youtube_analyzer/README.md) for detailed usage.

### RAG Chatbot (🚧 In Development)
Planned features:
- Vector database for storing video transcript chunks
- Embedding generation for semantic search
- LLM integration for natural language responses
- Context-aware question answering
- Session management for multi-turn conversations

## Architecture (Planned)

```
User Question
    ↓
Video URL Input → YouTube Analyzer → Extract transcript/metadata
    ↓
Chunk & Embed → Vector Database (ChromaDB/Pinecone/FAISS)
    ↓
User Query → Semantic Search → Retrieve relevant chunks
    ↓
LLM (GPT/Claude/Llama) → Generate contextual answer
    ↓
Response with timestamps
```

## Architecture

This project uses a **100% local and free** technology stack:

- **LLM**: Ollama + Llama 3.2 / Mistral (runs on your machine)
- **Embeddings**: sentence-transformers (local, no API)
- **Vector DB**: ChromaDB (embedded, no server)
- **Framework**: LangChain
- **UI**: Streamlit

**Total monthly cost: $0.00** 🎉

For detailed architecture documentation, see [ARCHITECTURE.md](ARCHITECTURE.md)

## Getting Started

**Quick Setup (~15 minutes):**

1. Install Ollama (local LLM):
   ```bash
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh

   # macOS
   brew install ollama

   # Windows: Download from https://ollama.ai
   ```

2. Pull an LLM model:
   ```bash
   ollama pull llama3.2  # ~2GB download
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Test the YouTube analyzer:
   ```bash
   cd youtube_analyzer
   python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --info
   ```

**For detailed setup instructions, see [SETUP.md](SETUP.md)**

### System Requirements

- **Minimum**: 8GB RAM, 15GB disk space, Python 3.9+
- **Recommended**: 16GB RAM, GPU optional (speeds up inference)

## Development Roadmap

- [x] YouTube video metadata extraction
- [x] Transcript/caption extraction
- [ ] Implement RAG pipeline
- [ ] Vector database integration
- [ ] LLM integration for Q&A
- [ ] Web interface
- [ ] Multi-video conversation support

## Contributing

This project is in active development. Contributions welcome!

## License

UNLICENSED
