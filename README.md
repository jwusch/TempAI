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

## Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd TempAI
   ```

2. Set up the YouTube analyzer:
   ```bash
   cd youtube_analyzer
   pip install -r requirements.txt
   ```

3. Test the analyzer:
   ```bash
   python3 youtube_analyzer.py "https://www.youtube.com/watch?v=VIDEO_ID" --info
   ```

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
