# app.py

import streamlit as st
from rag_engine import process_pdf_and_answer

# ── Page config ──────────────────────────────
st.set_page_config(
    page_title="RAG PDF Assistant",
    page_icon="📄",
    layout="centered"
)

# ── Header ───────────────────────────────────
st.title("📄 RAG PDF Assistant")
st.markdown("Upload a PDF and ask questions about it using AI.")
st.divider()

# ── Session state for chat history ───────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "collection_ready" not in st.session_state:
    st.session_state.collection_ready = False
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# ── Sidebar ───────────────────────────────────
with st.sidebar:
    st.header("📁 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        st.success(f"✅ {uploaded_file.name} uploaded!")
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. Upload a PDF")
    st.markdown("2. Ask any question")
    st.markdown("3. AI answers from the document")
    st.divider()
    st.caption("Built with LangChain · ChromaDB · Groq · Streamlit")

# ── Chat history display ──────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ── Chat input ────────────────────────────────
if query := st.chat_input("Ask a question about your PDF..."):
    if not st.session_state.uploaded_file:
        st.warning("⚠️ Please upload a PDF first!")
    else:
        # show user message
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # generate answer
        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                answer, pages, chunks = process_pdf_and_answer(
                    st.session_state.uploaded_file, query
                )
            st.markdown(answer)
            st.caption(f"📊 {pages} pages · {chunks} chunks searched")

        st.session_state.messages.append({"role": "assistant", "content": answer})