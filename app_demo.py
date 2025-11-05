"""TempAI Demo - Simplified version without ML dependencies
Shows the UI and flow without requiring sentence-transformers/PyTorch
"""

import streamlit as st
from pathlib import Path
import sys
import time

# Page configuration
st.set_page_config(
    page_title="TempAI Demo - Video Q&A",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'demo_videos' not in st.session_state:
    st.session_state.demo_videos = [
        {
            "video_id": "demo1",
            "title": "Introduction to Machine Learning",
            "channel": "AI Academy",
            "chunk_count": 45,
            "description": "This video covers the basics of machine learning, including supervised and unsupervised learning, neural networks, and practical applications."
        },
        {
            "video_id": "demo2",
            "title": "Building RAG Applications",
            "channel": "Tech Tutorials",
            "chunk_count": 67,
            "description": "A comprehensive guide to building Retrieval-Augmented Generation applications using vector databases and large language models."
        }
    ]

if 'current_video_id' not in st.session_state:
    st.session_state.current_video_id = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Demo Q&A responses
demo_responses = {
    "what is this about": "This video provides a comprehensive introduction to the topic, covering fundamental concepts and practical applications. It starts with the basics and progressively builds to more advanced topics.",
    "main points": "The main points discussed in this video are:\n1. Core concepts and definitions\n2. Practical applications and use cases\n3. Best practices and common pitfalls\n4. Future trends and developments",
    "summary": "This video offers an in-depth exploration of the subject matter, beginning with foundational principles and advancing through practical implementations. Key topics include theoretical frameworks, hands-on examples, and real-world applications.",
}

def get_demo_answer(question):
    """Generate a demo answer based on question keywords"""
    question_lower = question.lower()

    for keyword, response in demo_responses.items():
        if keyword in question_lower:
            return response

    # Default response
    return f"Based on the video content, here's what I found regarding '{question}':\n\nThe video discusses this topic in detail around the middle section. The presenter explains the concept thoroughly with examples and practical demonstrations. This is covered across multiple segments with supporting information and context."

# Header
st.markdown('<div class="main-header">🎥 TempAI Demo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Video Q&A Chatbot Interface Demo</div>', unsafe_allow_html=True)

# Info banner
st.info("ℹ️ **Demo Mode**: This is a simplified demo showing the interface. Full ML functionality requires additional packages (sentence-transformers, PyTorch) which couldn't be installed due to disk space limitations in this environment.")

# Sidebar
with st.sidebar:
    st.header("📚 Video Library")

    # Demo: Add new video
    with st.expander("➕ Add New Video", expanded=False):
        video_url = st.text_input(
            "YouTube URL",
            placeholder="https://www.youtube.com/watch?v=..."
        )

        col1, col2 = st.columns(2)
        with col1:
            chunk_size = st.number_input("Chunk Size", min_value=100, max_value=1000, value=500)
        with col2:
            chunk_overlap = st.number_input("Overlap", min_value=0, max_value=200, value=50)

        if st.button("🔄 Process Video (Demo)", use_container_width=True):
            if video_url:
                with st.spinner("Processing video..."):
                    time.sleep(2)  # Simulate processing
                    st.success("✅ Video processed! (Demo mode - would extract real transcript in full version)")
            else:
                st.warning("Please enter a YouTube URL")

    st.divider()

    # List demo videos
    st.subheader("Demo Videos")

    for video in st.session_state.demo_videos:
        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                if st.button(
                    f"📹 {video['title'][:40]}...",
                    key=f"select_{video['video_id']}",
                    use_container_width=True,
                    type="primary" if st.session_state.current_video_id == video['video_id'] else "secondary"
                ):
                    st.session_state.current_video_id = video['video_id']
                    st.session_state.chat_history = []
                    st.rerun()

            with col2:
                if st.button("🗑️", key=f"delete_{video['video_id']}"):
                    st.info("Delete button (demo)")

            st.caption(f"📊 {video['chunk_count']} chunks | 👤 {video['channel']}")

    st.divider()

    # Settings
    with st.expander("⚙️ Settings"):
        llm_model = st.selectbox(
            "LLM Model",
            ["llama3.2", "llama3.1", "mistral", "llama3.2:1b"],
            index=0
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1,
            help="Lower = more factual, Higher = more creative"
        )

        top_k = st.slider(
            "Top K Results",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of relevant chunks to retrieve"
        )

# Main content
if st.session_state.current_video_id is None:
    # No video selected
    st.info("👈 Please select a demo video from the sidebar to start!")

    st.markdown("""
    ## TempAI Demo Interface

    This is a demonstration of the TempAI user interface. In the full version, this application:

    ### Features

    ✅ **Video Processing**
    - Extracts transcripts from YouTube videos
    - Chunks text into manageable pieces
    - Generates embeddings using sentence-transformers
    - Stores in ChromaDB vector database

    ✅ **Question Answering**
    - Semantic search through video content
    - Retrieves relevant chunks based on your question
    - Generates contextual answers using local LLM (Ollama)
    - Provides source citations with timestamps

    ✅ **100% Local & Free**
    - No API costs ($0/month vs $100+/month for cloud)
    - Complete privacy - data never leaves your machine
    - No rate limits
    - Works offline after initial setup

    ### Full Installation Requirements

    To run the complete application on your local machine:

    ```bash
    # 1. Install Ollama (local LLM)
    curl -fsSL https://ollama.ai/install.sh | sh
    ollama pull llama3.2

    # 2. Install Python dependencies
    pip install streamlit chromadb sentence-transformers ollama yt-dlp

    # 3. Run the app
    streamlit run app.py
    ```

    ### Why This Demo?

    The full application requires ~15GB of disk space for ML packages (PyTorch, transformers).
    This containerized environment has limited space, so this demo shows the interface without
    the ML backend.

    **All code is complete and committed to the repository!** You can run the full version on
    your local machine with the installation steps above.
    """)

else:
    # Video selected
    current_video = next((v for v in st.session_state.demo_videos if v['video_id'] == st.session_state.current_video_id), None)

    if current_video:
        # Video info
        st.markdown(f"### 📹 {current_video['title']}")
        st.caption(f"👤 {current_video['channel']} | 📊 {current_video['chunk_count']} chunks")

        st.divider()

        # Chat history
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat['question'])

            with st.chat_message("assistant"):
                st.write(chat['answer'])

                if chat.get('sources'):
                    with st.expander("📚 View Sources"):
                        for source in chat['sources']:
                            st.markdown(f"""
                            **{source['timestamp']}** (Relevance: {source['relevance']:.2f})
                            > {source['preview']}
                            """)

        # Question input
        question = st.chat_input("Ask a question about this video... (Demo mode)")

        if question:
            # Add user question
            with st.chat_message("user"):
                st.write(question)

            # Generate demo answer
            with st.chat_message("assistant"):
                with st.spinner("Thinking... (Demo mode)"):
                    time.sleep(1.5)  # Simulate processing

                    answer = get_demo_answer(question)
                    st.write(answer)

                    # Demo sources
                    with st.expander("📚 View Sources (Demo)"):
                        st.markdown("""
                        **Part 12** (Relevance: 0.89)
                        > This section discusses the key concepts in detail, providing examples and explaining the underlying principles...

                        **Part 24** (Relevance: 0.82)
                        > Here the presenter elaborates on practical applications, showing how the theory translates to real-world scenarios...

                        **Part 31** (Relevance: 0.76)
                        > Additional context and supporting information that helps clarify the main concepts discussed earlier...
                        """)

                    # Add to history
                    st.session_state.chat_history.append({
                        'question': question,
                        'answer': answer,
                        'sources': [
                            {'timestamp': 'Part 12', 'relevance': 0.89, 'preview': 'This section discusses...'},
                            {'timestamp': 'Part 24', 'relevance': 0.82, 'preview': 'Here the presenter...'},
                            {'timestamp': 'Part 31', 'relevance': 0.76, 'preview': 'Additional context...'},
                        ]
                    })

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    TempAI v0.1.0 Demo | Full version requires: Ollama + ChromaDB + sentence-transformers | 100% Local & Free
</div>
""", unsafe_allow_html=True)
