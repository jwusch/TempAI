# How to Access TempAI

The application is currently running in a containerized Claude Code environment where ports are not exposed externally. Here's how to access it:

## 🚀 Quick Access (5 minutes)

### Option 1: Demo Version (No AI, Just UI)

Run this on **your local machine**:

```bash
# 1. Pull the latest code
git pull origin claude/investigate-repo-011CUqTJu2yzTA79ThTdY62h

# 2. Install Streamlit
pip install streamlit

# 3. Run the demo
streamlit run app_demo.py
```

✨ **Your browser will automatically open to http://localhost:8501**

**What you get:**
- Full working interface
- Demo videos pre-loaded
- Mock Q&A responses (no real AI)
- All UI features functional

---

## 🤖 Full Version (With Real AI)

For the complete experience with actual video processing and AI:

### Step 1: Install Ollama (One-time setup)

**Linux/macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai/download

### Step 2: Download AI Model

```bash
# Download Llama 3.2 (recommended, ~2GB)
ollama pull llama3.2

# Verify it works
ollama run llama3.2
# Type "hello" and press Enter
# Type "/bye" to exit
```

### Step 3: Install Python Dependencies

```bash
pip install streamlit chromadb sentence-transformers ollama yt-dlp
```

**Note:** This downloads PyTorch and ML models (~2-4GB total)

### Step 4: Run the Full App

```bash
streamlit run app.py
```

✨ **Browser opens to http://localhost:8501 with full AI capabilities!**

---

## 📱 What You Can Do

### Demo Version (`app_demo.py`)
- ✅ See the complete interface
- ✅ Navigate between videos
- ✅ Type questions and get mock responses
- ✅ View source citations
- ❌ No real video processing
- ❌ No actual AI responses

### Full Version (`app.py`)
- ✅ Process real YouTube videos
- ✅ Extract actual transcripts
- ✅ Ask questions about video content
- ✅ Get AI-generated answers with sources
- ✅ Store multiple videos
- ✅ 100% local, no API costs

---

## 🎯 Example Workflow (Full Version)

1. **Start the app**: `streamlit run app.py`
2. **Add a video**:
   - Paste: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Click "Process Video"
   - Wait ~30 seconds
3. **Ask questions**:
   - "What is this video about?"
   - "What are the main points?"
   - "Summarize the key topics"
4. **Get answers** in 3-6 seconds with source citations!

---

## 🔧 Troubleshooting

### "Port 8501 is already in use"
```bash
# Find and kill the process
lsof -i :8501
kill -9 <PID>

# Or use a different port
streamlit run app.py --server.port 8502
```

### "Ollama is not running"
```bash
# Start Ollama
ollama serve

# In another terminal, verify
ollama list
```

### "No module named 'streamlit'"
```bash
# Make sure you're in the right directory
cd TempAI

# Install dependencies
pip install streamlit
```

---

## 💡 Why Can't I Access It in Claude Code?

The Streamlit app IS running in this containerized environment on port 8501, but:

- ❌ The container doesn't expose ports externally
- ❌ No port forwarding configured
- ❌ Network is isolated from your browser

**Solution:** Run it on your local machine where you have full network access!

---

## 📊 System Requirements

**Demo Version:**
- Python 3.9+
- ~100MB RAM
- ~10MB disk

**Full Version:**
- Python 3.9+
- 8GB RAM (16GB recommended)
- 15GB disk space
- Ollama installed

---

## 🎉 Summary

**To access TempAI:**

1. **Quick Preview (Demo)**: `streamlit run app_demo.py` on your machine
2. **Full Experience**: Install Ollama + dependencies, then `streamlit run app.py`
3. **Access**: Your browser automatically opens to `http://localhost:8501`

All code is committed and ready to use! 🚀
