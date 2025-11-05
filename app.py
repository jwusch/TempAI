"""TempAI - Video Q&A RAG Chatbot
Streamlit web interface for asking questions about YouTube videos
"""

import streamlit as st
from pathlib import Path
import sys

# Add rag_chatbot to path
sys.path.append(str(Path(__file__).parent))

from rag_chatbot.video_processor import VideoProcessor
from rag_chatbot.qa_engine import QAEngine


# Page configuration
st.set_page_config(
    page_title="TempAI - Video Q&A",
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
    .video-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #ddd;
        margin-bottom: 1rem;
    }
    .source-card {
        padding: 0.75rem;
        border-radius: 0.3rem;
        background-color: #f0f0f0;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'video_processor' not in st.session_state:
    st.session_state.video_processor = VideoProcessor()

if 'qa_engine' not in st.session_state:
    st.session_state.qa_engine = QAEngine()

if 'current_video_id' not in st.session_state:
    st.session_state.current_video_id = None

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


# Header
st.markdown('<div class="main-header">🎥 TempAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask questions about YouTube videos using AI</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📚 Video Library")

    # Add new video
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

        if st.button("🔄 Process Video", use_container_width=True):
            if video_url:
                with st.spinner("Processing video..."):
                    result = st.session_state.video_processor.process_video(
                        video_url,
                        chunk_size=chunk_size,
                        chunk_overlap=chunk_overlap
                    )

                    if result['status'] == 'success':
                        st.success(f"✅ Processed: {result['video_info']['title']}")
                        st.session_state.current_video_id = result['video_id']
                        st.rerun()
                    elif result['status'] == 'already_exists':
                        st.info(f"ℹ️ Video already processed")
                        st.session_state.current_video_id = result['video_id']
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
            else:
                st.warning("Please enter a YouTube URL")

    st.divider()

    # List processed videos
    st.subheader("Processed Videos")
    videos = st.session_state.video_processor.list_processed_videos()

    if videos:
        for video in videos:
            with st.container():
                col1, col2 = st.columns([4, 1])

                with col1:
                    # Create a button for each video
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
                    # Delete button
                    if st.button("🗑️", key=f"delete_{video['video_id']}"):
                        if st.session_state.video_processor.delete_video(video['video_id']):
                            st.success("Deleted!")
                            if st.session_state.current_video_id == video['video_id']:
                                st.session_state.current_video_id = None
                                st.session_state.chat_history = []
                            st.rerun()

                st.caption(f"📊 {video['chunk_count']} chunks | 👤 {video['channel']}")
    else:
        st.info("No videos processed yet. Add one above!")

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

        # Update QA engine settings
        st.session_state.qa_engine.llm_model = llm_model
        st.session_state.qa_engine.top_k = top_k


# Main content
if st.session_state.current_video_id is None:
    # No video selected - show instructions
    st.info("👈 Please add and select a video from the sidebar to start asking questions!")

    st.markdown("""
    ## How to use TempAI

    1. **Add a video**: Enter a YouTube URL in the sidebar and click "Process Video"
    2. **Select the video**: Click on the video title in the sidebar
    3. **Ask questions**: Type your question about the video content
    4. **Get answers**: AI will answer based on the video transcript

    ### System Requirements
    - Ollama must be running locally
    - Model downloaded (e.g., `ollama pull llama3.2`)

    ### Features
    - 100% local and free - no API costs
    - Private - data never leaves your machine
    - Fast responses (~3-6 seconds)
    - Timestamped sources
    """)

else:
    # Video selected - show Q&A interface
    videos = st.session_state.video_processor.list_processed_videos()
    current_video = next((v for v in videos if v['video_id'] == st.session_state.current_video_id), None)

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
                        for i, source in enumerate(chat['sources'][:3]):
                            st.markdown(f"""
                            **{source['timestamp']}** (Relevance: {source['relevance_score']:.2f})
                            > {source['text_preview']}
                            """)

        # Question input
        question = st.chat_input("Ask a question about this video...")

        if question:
            # Add user question to chat
            with st.chat_message("user"):
                st.write(question)

            # Generate answer
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    result = st.session_state.qa_engine.answer_question(
                        question=question,
                        video_id=st.session_state.current_video_id,
                        temperature=temperature
                    )

                    if result['status'] in ['success', 'no_llm', 'llm_error']:
                        st.write(result['answer'])

                        # Show sources
                        if result.get('sources'):
                            with st.expander("📚 View Sources"):
                                for i, source in enumerate(result['sources'][:3]):
                                    st.markdown(f"""
                                    **{source['timestamp']}** (Relevance: {source['relevance_score']:.2f})
                                    > {source['text_preview']}
                                    """)

                        # Add to chat history
                        st.session_state.chat_history.append({
                            'question': question,
                            'answer': result['answer'],
                            'sources': result.get('sources', [])
                        })

                    else:
                        st.error(f"❌ {result.get('error', 'Unknown error')}")

    else:
        st.error("Selected video not found. Please select another video.")


# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem;">
    TempAI v0.1.0 | 100% Local & Free | Powered by Ollama + ChromaDB + LangChain
</div>
""", unsafe_allow_html=True)
