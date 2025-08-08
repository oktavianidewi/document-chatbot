import psycopg
import os

# Database connection configs
DB_NAME = os.getenv("PG_DATABASE", "chatbot_db")
DB_USER = os.getenv("PG_USER", "chatbot")
DB_PASSWORD = os.getenv("PG_PASSWORD", "chatbot")
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", 5432)

DB_CONFIG = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT,
}

def create_database():
    """Create database if it doesn't exist."""
    conn = psycopg.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()

    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME};")
        print(f"✅ Database '{DB_NAME}' created.")
    else:
        print(f"ℹ️ Database '{DB_NAME}' already exists.")

    cur.close()
    conn.close()


def migrate_up():
    """Create tables for RAG pipeline."""
    create_database()
    DB_CONFIG['dbname'] = DB_NAME  # Add database name to config
    conn = psycopg.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS public.documents (
            doc_id SERIAL PRIMARY KEY,
            title TEXT,
            source_path TEXT,
            uploaded_at TIMESTAMP DEFAULT NOW()
        );
        """)
    except Exception as e:
        print(f"❌ Error creating 'documents' table: {e}")
        return
    try:
        cur.execute(f"""
        CREATE TABLE IF NOT EXISTS public.doc_chunks (
            chunk_id SERIAL PRIMARY KEY,
            doc_id INT REFERENCES public.documents(doc_id) ON DELETE CASCADE,
            chunk_text TEXT,
            embedding_id INT
        );
        """)
    except Exception as e:
        print(f"❌ Error creating 'documents' table: {e}")
        return

    conn.commit()
    cur.close()
    conn.close()
    print("✅ migrate_up completed: tables created.")


def migrate_down():
    """Drop all tables (rollback)."""
    conn = psycopg.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS doc_chunks CASCADE;")
    cur.execute("DROP TABLE IF EXISTS documents CASCADE;")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ migrate_down completed: tables dropped.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Database Migration Tool")
    parser.add_argument("action", choices=["up", "down"], help="Migrate up or down")
    args = parser.parse_args()

    if args.action == "up":
        migrate_up()
    else:
        migrate_down()
