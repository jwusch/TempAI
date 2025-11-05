# Quick Start Guide - TempAI

Get up and running with TempAI in 5 minutes!

## Prerequisites Check

Before starting, verify you have:

```bash
# Check Python version (need 3.9+)
python3 --version

# Check pip is available
pip --version
```

## Installation Steps

### 1. Install Python Dependencies (~5-10 minutes)

The installation includes some large ML packages (PyTorch, transformers), so it may take a while:

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install streamlit chromadb sentence-transformers ollama yt-dlp requests
```

**Note**: If installation takes too long or fails, try installing without PyTorch GPU support:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install streamlit chromadb sentence-transformers ollama yt-dlp requests
```

### 2. Install Ollama (The Local LLM)

Ollama runs the AI model locally on your machine.

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

**Windows:**
Download from https://ollama.ai/download

### 3. Download an AI Model (~2GB)

```bash
# Download Llama 3.2 (recommended - fast and good quality)
ollama pull llama3.2

# Or download Mistral (alternative)
ollama pull mistral

# Verify it works
ollama run llama3.2
# Type: "Hello!" and press Enter
# Type: "/bye" to exit
```

### 4. Run TempAI!

```bash
# Start the application
streamlit run app.py

# Your browser should open automatically to:
# http://localhost:8501
```

## First Use

### Add Your First Video

1. In the sidebar, click "➕ Add New Video"
2. Paste a YouTube URL (example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
3. Click "🔄 Process Video"
4. Wait ~30 seconds for processing

### Ask Questions

1. Click on the processed video in the sidebar
2. Type your question in the chat box
3. Press Enter and wait ~3-6 seconds
4. View the answer with source citations!

## Example Questions

- "What is this video about?"
- "What are the main points discussed?"
- "Can you summarize the key takeaways?"
- "What did they say about [specific topic]?"

## Troubleshooting

### "Ollama is not available"

Make sure Ollama is running:

```bash
# Check if running
ps aux | grep ollama

# Start Ollama (if not running)
ollama serve

# In another terminal, verify models are available
ollama list
```

### "Unable to extract video info"

The video might be:
- Private or age-restricted
- Region-blocked
- Removed

Try a different public video.

### "No transcript or description available"

Some videos don't have transcripts. Try:
- Videos with auto-generated captions
- Educational/tutorial videos (usually have good transcripts)
- Avoid music-only videos

### Python import errors

Reinstall dependencies:

```bash
pip install --upgrade -r requirements.txt
```

### App won't start

```bash
# Check if port 8501 is in use
lsof -i :8501

# Use a different port
streamlit run app.py --server.port 8502
```

## Performance Tips

### Speed Up Processing

1. **Use GPU**: If you have an NVIDIA GPU:
   ```bash
   # Uninstall CPU PyTorch
   pip uninstall torch

   # Install CUDA PyTorch
   pip install torch --index-url https://download.pytorch.org/whl/cu118
   ```

2. **Use smaller model**: In Settings sidebar, switch to `llama3.2:1b` (faster but less capable)

3. **Reduce chunk overlap**: Use 25 instead of 50 when processing videos

### Save Memory

1. **Use smaller model**: `llama3.2:1b` uses ~2GB instead of 4GB
2. **Close other applications**
3. **Process videos one at a time**

## What to Try

1. **Educational videos**: Try a TED talk or tutorial
2. **Podcast episodes**: Works great with interview/discussion content
3. **Lectures**: Academic content with good transcripts
4. **Product reviews**: Ask specific questions about features
5. **Documentaries**: Ask about facts and details

## Common Use Cases

### Research
- "What statistics were mentioned?"
- "What sources did they cite?"
- "What evidence supports [claim]?"

### Learning
- "Explain [concept] from the video"
- "What steps were described for [process]?"
- "What examples were given?"

### Summarization
- "Summarize the main argument"
- "What are the 3 key takeaways?"
- "What conclusion did they reach?"

## System Requirements Reminder

- **Minimum**: 8GB RAM, 15GB disk, CPU only
- **Recommended**: 16GB RAM, GPU optional
- **Model storage**: ~2-8GB per Ollama model
- **Per video**: ~10MB in ChromaDB

## Next Steps

Once comfortable with basics:

1. **Try different LLM models** in Settings
2. **Adjust temperature** for more creative vs factual answers
3. **Change Top K** to retrieve more/fewer context chunks
4. **Process multiple videos** and switch between them

## Getting Help

- **Ollama issues**: https://github.com/ollama/ollama/issues
- **ChromaDB issues**: https://github.com/chroma-core/chroma/issues
- **TempAI issues**: Check SETUP.md or ARCHITECTURE.md

## Privacy & Data

- ✅ All processing is local
- ✅ No data sent to external servers
- ✅ Works offline (after setup)
- ✅ Your questions and videos stay on your machine

## Cost

**$0.00/month** 🎉

Everything runs locally - no subscriptions, no API fees!

---

**Enjoy using TempAI!** 🚀
