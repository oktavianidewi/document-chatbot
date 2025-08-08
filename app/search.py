import faiss
import numpy as np
import json
import psycopg
from pathlib import Path
from sentence_transformers import SentenceTransformer
import os

# ========== CONFIG ==========
DB_NAME = os.getenv("PG_DATABASE", "chatbot_db")
DB_USER = os.getenv("PG_USER", "chatbot")
DB_PASSWORD = os.getenv("PG_PASSWORD", "chatbot")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", 5432)

DB_CONFIG = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
}
FAISS_INDEX_PATH = Path("models/faiss_index/aws.index")
CHUNKS_FILE = Path("data/chunks.json")
EMBED_MODEL = "all-MiniLM-L6-v2"
# ============================

model = SentenceTransformer(EMBED_MODEL)

# Load FAISS index
if not FAISS_INDEX_PATH.exists():
    raise FileNotFoundError("FAISS index not found. Run ingest.py first.")
index = faiss.read_index(str(FAISS_INDEX_PATH))

# Connect to PostgreSQL
conn = psycopg.connect(**DB_CONFIG)
cur = conn.cursor()

def search(query: str, k: int = 3):
    """Search top-k chunks by semantic similarity and return text with metadata."""
    embedding = model.encode([query]).astype("float32")
    D, I = index.search(embedding, k)

    results = []
    for idx in I[0]:
        # Get chunk text + metadata from PostgreSQL
        cur.execute("""
            SELECT c.chunk_text, d.title, d.source_path
            FROM doc_chunks c
            JOIN documents d ON c.doc_id = d.doc_id
            WHERE c.embedding_id = %s
        """, (int(idx),))
        row = cur.fetchone()
        if row:
            chunk_text, title, source = row
            results.append({
                "chunk": chunk_text,
                "title": title,
                "source": source
            })

    return results

if __name__ == "__main__":
    import argparse, json

    parser = argparse.ArgumentParser(description="Test FAISS + PostgreSQL Search")
    parser.add_argument("query", help="Search query string")
    parser.add_argument("--k", type=int, default=3, help="Number of chunks to retrieve")
    args = parser.parse_args()

    results = search(args.query, k=args.k)
    print(json.dumps(results, indent=2, ensure_ascii=False))
