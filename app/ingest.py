import os
import json
import psycopg
import faiss
from pathlib import Path
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import textwrap

# ============ CONFIG ============
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

RAW_DATA_DIR = Path("data/raw")

FAISS_INDEX = "models/faiss_index/aws.index"
FAISS_INDEX_PATH = Path(FAISS_INDEX)
FAISS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

EMBED_MODEL = 'all-MiniLM-L6-v2'
CHUNK_SIZE = 400  # approx chars per chunk
# ================================

conn = psycopg.connect(**DB_CONFIG)
cur = conn.cursor()



def chunk_text(text, chunk_size=CHUNK_SIZE):
    """Split text into smaller chunks."""
    return textwrap.wrap(text, chunk_size)

def ingest_document(file_path: Path):
    print(f"Ingesting {file_path.name}...")

    # 1. Read file
    if file_path.suffix.lower() == ".pdf":
        reader = PdfReader(file_path)
        full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        with open(file_path, "r") as f:
            full_text = f.read()

    # 2. Chunk text
    chunks = chunk_text(full_text)

    # 3. Embed
    embeddings = model.encode(chunks).astype("float32")
    start_id = index.ntotal
    index.add(embeddings)  # store in FAISS

    # 4. Store metadata in PostgreSQL
    cur.execute(
        "INSERT INTO documents (title, source_path) VALUES (%s, %s) RETURNING doc_id",
        (file_path.stem, str(file_path)),
    )
    doc_id = cur.fetchone()[0]

    for i, chunk in enumerate(chunks):
        embedding_id = start_id + i
        cur.execute(
            """
            INSERT INTO doc_chunks (doc_id, chunk_text, embedding_id)
            VALUES (%s, %s, %s)
            """,
            (doc_id, chunk, embedding_id),
        )

    conn.commit()
    print(f"✅ Ingested {len(chunks)} chunks from {file_path.name}")

if __name__ == "__main__":
    model = SentenceTransformer(EMBED_MODEL)

    # Load or create FAISS index
    dim = model.get_sentence_embedding_dimension()
    index = faiss.IndexFlatL2(dim)
    if Path(FAISS_INDEX_PATH).exists():
        index = faiss.read_index(FAISS_INDEX)
        print(f"✅ Loaded existing FAISS index from {FAISS_INDEX_PATH}")
    else:
        index = faiss.IndexFlatL2(dim)
        faiss.write_index(index, FAISS_INDEX)
        print(f"✅ Created new FAISS index with dimension {dim}")

    RAW_DATA_DIR.mkdir(exist_ok=True)
    files = list(RAW_DATA_DIR.glob("*.pdf")) + list(RAW_DATA_DIR.glob("*.txt"))
    if not files:
        print("⚠️ No files in data/raw/ to ingest.")
    else:
        for f in files:
            print(f"Processing {f.name}...")
            ingest_document(f)
        faiss.write_index(index, FAISS_INDEX)
        print("✅ FAISS index saved.")
