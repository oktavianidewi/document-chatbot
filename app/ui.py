import streamlit as st
from search import search
from rag_chain import ask

st.set_page_config(page_title="AWS RAG Chatbot", layout="wide")
st.title("🤖 AWS RAG Chatbot")

st.markdown(
    """
    Ask questions about AWS services.  
    This chatbot uses **RAG**: retrieves from local AWS docs + answers with LLM.
    """
)

# Sidebar
with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Top K Chunks", 1, 10, 3)
    show_chunks = st.checkbox("Show retrieved chunks (debug)", value=True)

query = st.text_input("Ask about AWS services:", placeholder="e.g., What is Amazon S3?")

if query:
    with st.spinner("Searching documents and generating answer..."):
        # 1️⃣ Retrieve chunks
        chunks = search(query, k=top_k)

        # 2️⃣ Get LLM answer
        answer = ask(query)

        # 3️⃣ Display answer
        st.markdown("### 📥 LLM Answer")
        st.write(answer)

        # 4️⃣ Optional debug view
        # if show_chunks:
        #     st.markdown("---")
        #     st.markdown("### 🔍 Retrieved Chunks")
        #     for i, c in enumerate(chunks, start=1):
        #         st.markdown(f"**Chunk {i}:** {c[:500]}...")

st.markdown("---")
st.caption("Powered by FAISS + PostgreSQL + Ollama/OpenAI fallback")
