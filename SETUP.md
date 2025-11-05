# TempAI Setup Guide - Local & Free RAG System

This guide will help you set up TempAI completely locally with zero cost. Total setup time: ~15-30 minutes.

## Prerequisites

### System Requirements

**Minimum:**
- OS: Linux, macOS, or Windows 10+
- RAM: 8GB (16GB recommended)
- Storage: 15GB free space
- CPU: Multi-core processor (4+ cores recommended)
- Internet: Required for initial setup only

**Optional (for better performance):**
- NVIDIA GPU with 4GB+ VRAM
- CUDA 11.8+ installed

### Software Requirements

- Python 3.9 or higher
- pip (Python package manager)
- git

Check your Python version:
```bash
python3 --version  # Should show 3.9.0 or higher
```

## Step-by-Step Installation

### Step 1: Install Ollama (Local LLM)

Ollama is the local LLM runtime that runs Llama, Mistral, and other open models.

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS
```bash
# Using Homebrew
brew install ollama

# Or download from website
# Visit: https://ollama.ai/download
```

#### Windows
1. Download from https://ollama.ai/download
2. Run the installer
3. Ollama will run as a background service

**Verify Ollama is running:**
```bash
ollama --version
# Should show: ollama version is 0.x.x
```

### Step 2: Download LLM Models

Download Llama 3.2 (recommended) or Mistral:

```bash
# Llama 3.2 (3B parameters, ~2GB) - Fast and efficient
ollama pull llama3.2

# OR Mistral (7B parameters, ~4GB) - More capable but slower
ollama pull mistral

# OR both if you have space
ollama pull llama3.2
ollama pull mistral
```

**Test the model:**
```bash
ollama run llama3.2
# Type a message, then /bye to exit
```

**Model sizes:**
- `llama3.2:1b` - 1.3GB (very fast, basic quality)
- `llama3.2` (3b) - 2GB (good balance) ⭐ **Recommended**
- `llama3.1:8b` - 4.7GB (better quality, slower)
- `mistral` - 4.1GB (alternative, good quality)
- `llama3.1:70b` - 40GB (best quality, requires 64GB RAM)

### Step 3: Clone TempAI Repository

```bash
git clone https://github.com/jwusch/TempAI.git
cd TempAI
```

### Step 4: Set Up Python Environment

#### Using venv (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Using conda (Alternative)

```bash
conda create -n tempai python=3.11
conda activate tempai
```

### Step 5: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This will download:
# - LangChain (~50MB)
# - ChromaDB (~30MB)
# - sentence-transformers (~100MB)
# - Streamlit (~40MB)
# - yt-dlp and other utilities
```

**Note for GPU users:**
If you have an NVIDIA GPU, install PyTorch with CUDA:
```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Step 6: Download Embedding Model

The embedding model will download automatically on first use, but you can pre-download it:

```bash
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

This downloads ~80MB to `~/.cache/torch/sentence_transformers/`

### Step 7: Verify Installation

Run the verification script:

```bash
python3 -c "
import chromadb
import ollama
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
print('✅ All imports successful!')
print('✅ ChromaDB version:', chromadb.__version__)
print('✅ Checking Ollama...')
try:
    ollama.list()
    print('✅ Ollama is running!')
except:
    print('❌ Ollama is not running. Start it with: ollama serve')
"
```

Expected output:
```
✅ All imports successful!
✅ ChromaDB version: 0.4.22
✅ Checking Ollama...
✅ Ollama is running!
```

## Quick Start

### Test the YouTube Analyzer

```bash
cd youtube_analyzer
python3 youtube_analyzer.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --info
```

This should display video information without errors.

### Run the RAG Chatbot (Coming Soon)

Once the RAG pipeline is implemented:

```bash
# Start the Streamlit app
streamlit run app.py

# Opens in browser at http://localhost:8501
```

## Configuration

### Optional: Environment Variables

Create a `.env` file in the project root:

```bash
# TempAI Configuration

# Ollama settings
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2

# ChromaDB settings
CHROMADB_PERSIST_DIR=./data/chromadb

# Embedding model
EMBEDDING_MODEL=all-MiniLM-L6-v2

# RAG settings
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RESULTS=5

# UI settings
STREAMLIT_PORT=8501
```

### Customize Models

Edit the model in your code or environment:

```python
# Use Mistral instead of Llama
OLLAMA_MODEL=mistral

# Use a larger embedding model (slower but better)
EMBEDDING_MODEL=all-mpnet-base-v2
```

## Troubleshooting

### Ollama Issues

**Problem: "Connection refused" or "Ollama not running"**

```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama manually (Linux/macOS)
ollama serve

# On Windows, restart the Ollama service
```

**Problem: "Model not found"**

```bash
# List installed models
ollama list

# Pull the model again
ollama pull llama3.2
```

### Python Dependency Issues

**Problem: "No module named 'chromadb'"**

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Problem: PyTorch/CUDA errors**

```bash
# For CPU-only (no GPU)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# For CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

### YouTube Download Issues

**Problem: "Unable to extract video info"**

1. Update yt-dlp:
   ```bash
   pip install --upgrade yt-dlp
   ```

2. Try with `--no-check-certificate` flag (see youtube_analyzer README)

3. Check if the video has restrictions (age, region, private)

### Memory Issues

**Problem: "Killed" or "Out of memory"**

1. Use a smaller model:
   ```bash
   ollama pull llama3.2:1b  # Smaller 1B parameter version
   ```

2. Close other applications

3. Reduce batch size in code (if processing multiple videos)

### ChromaDB Issues

**Problem: "Database locked"**

```bash
# Stop any running ChromaDB processes
pkill -f chromadb

# Delete the lock file
rm data/chromadb/*.lock
```

**Problem: Corrupted database**

```bash
# Backup and reset
mv data/chromadb data/chromadb.backup
mkdir data/chromadb
# Re-process your videos
```

## Performance Optimization

### Speed Up Embeddings

1. Use GPU if available (automatic with CUDA)
2. Use a smaller model: `all-MiniLM-L6-v2` (default, fast)
3. Batch process multiple chunks

### Speed Up LLM Inference

1. Use smaller model: `llama3.2:1b`
2. Reduce max_tokens in generation
3. Use GPU with Ollama (automatic if available)

### Reduce Memory Usage

1. Use quantized models (Ollama does this by default)
2. Close unused applications
3. Process videos one at a time
4. Use `llama3.2:1b` (uses ~2GB instead of 4GB)

## Next Steps

After successful installation:

1. ✅ Test the YouTube analyzer on a few videos
2. ✅ Verify Ollama responds to prompts
3. ✅ Run the verification script
4. 🚧 Wait for RAG pipeline implementation
5. 🚧 Start using the Streamlit interface

## Updating

### Update Ollama Models

```bash
# Pull latest version of a model
ollama pull llama3.2
```

### Update Python Dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Update TempAI

```bash
git pull origin main
pip install -r requirements.txt  # In case dependencies changed
```

## Uninstalling

### Remove Everything

```bash
# Remove Ollama models
ollama rm llama3.2
ollama rm mistral

# Remove Ollama (Linux)
sudo rm -rf /usr/local/bin/ollama
sudo rm -rf /usr/local/lib/ollama

# Remove Ollama (macOS)
brew uninstall ollama

# Remove Ollama (Windows)
# Use Windows "Add or Remove Programs"

# Remove Python dependencies
pip uninstall -r requirements.txt -y

# Remove project directory
cd ..
rm -rf TempAI

# Remove cached models
rm -rf ~/.cache/torch/sentence_transformers
rm -rf ~/.ollama
```

## Getting Help

- **Ollama Issues**: https://github.com/ollama/ollama/issues
- **ChromaDB Issues**: https://github.com/chroma-core/chroma/issues
- **TempAI Issues**: https://github.com/jwusch/TempAI/issues

## Cost Breakdown

| Component | Cost |
|-----------|------|
| Ollama | **FREE** |
| Python packages | **FREE** |
| Models (Llama, embeddings) | **FREE** |
| ChromaDB | **FREE** |
| Storage (~15GB) | **FREE** (you provide) |
| Internet (setup only) | ~1GB download |
| **Total monthly cost** | **$0.00** |

Compare to cloud alternatives:
- GPT-4 API: $0.03 per 1K tokens (~$30-100/month typical usage)
- Claude API: $0.015 per 1K tokens (~$15-50/month)
- Pinecone: $70/month (starter plan)

🎉 **You just saved ~$100+/month!**
