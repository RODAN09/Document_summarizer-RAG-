📄 Document Summarizer — RAG PDF Assistant
A Retrieval-Augmented Generation (RAG) application that lets you upload any PDF document and ask questions about it using AI. Built with a fully free tech stack.

🚀 Live Demo
Deployed on Render: https://document-summarizer-rag-2.onrender.com


🧠 How It Works
PDF Upload → Extract Text → Chunk Text → Create Embeddings
                                                ↓
User Question → Embed Question → Search ChromaDB → Retrieve Top Chunks
                                                ↓
                              Chunks + Question → Groq LLM → Answer

Upload a PDF document via the sidebar
The app extracts and splits text into 500-character chunks with 50-character overlap
Each chunk is converted into a vector embedding using all-MiniLM-L6-v2
Embeddings are stored in ChromaDB (in-memory vector database)
When you ask a question, it is embedded and the top 3 most relevant chunks are retrieved
Retrieved chunks + your question are sent to the Groq LLM for a grounded answer

