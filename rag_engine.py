# rag_engine.py

import os
os.environ["USE_TF"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
CHUNK_SIZE    = 500
CHUNK_OVERLAP = 50
TOP_K         = 3

embedder   = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()


def load_pdf(file):
    reader = PdfReader(file)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text, len(reader.pages)


def chunk_text(text):
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunks.append(text[start:end])
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def build_vector_store(chunks, collection_name="rag_docs"):
    # delete old collection if exists
    try:
        chroma_client.delete_collection(collection_name)
    except:
        pass

    collection = chroma_client.create_collection(collection_name)
    embeddings = embedder.encode(chunks).tolist()

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    return collection


def retrieve(query, collection):
    query_embedding = embedder.encode([query]).tolist()
    result = collection.query(
        query_embeddings=query_embedding,
        n_results=TOP_K
    )
    return result["documents"][0]


def generate_answer(query, retrieved_chunks):
    client = Groq(api_key=GROQ_API_KEY)
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""You are a helpful assistant. Answer the user's question ONLY based on the context below.
If the answer is not in the context, say "I don't have enough information in the document."

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def process_pdf_and_answer(uploaded_file, query):
    text, pages = load_pdf(uploaded_file)
    chunks = chunk_text(text)
    collection = build_vector_store(chunks)
    retrieved = retrieve(query, collection)
    answer = generate_answer(query, retrieved)
    return answer, pages, len(chunks)