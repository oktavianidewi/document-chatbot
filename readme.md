# 📚 Local RAG Chatbot for AWS Docs

This project is a **Retrieval-Augmented Generation (RAG)** chatbot you can run entirely on your machine. It can answer context-related questions using your own documents (PDF/TXT) as a knowledge base.

### 🔹 Features

* Converts PDFs/TXT into embeddings with **FAISS**
* Saves chunk metadata in **PostgreSQL**
* Runs on a **local LLM via Ollama** (with OpenAI as fallback)
* Provides a **Streamlit** chat UI with chat bubbles

### 🛠 Tech Stack

* **Ollama** → Run LLM locally without API keys
* **Streamlit** → Interactive web chat interface
* **Python** → RAG pipeline for loading, embedding, searching, and generating answers
* **PostgreSQL** → Store metadata for document chunks

💡 *RAG allows an LLM to use external sources (like PDFs) to give accurate, context-aware answers.*

---

## 📦 1. Requirements

Make sure you have:

* **WSL** (Windows users) → [Install guide](https://learn.microsoft.com/en-us/windows/wsl/install)
* **Git**

  * Linux/WSL → [Guide](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git)
  * Mac → `brew install git`
* **Docker Desktop**

  * [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
  * [Linux](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)
  * [Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
* **Docker CLI** → [Linux Install](https://docs.docker.com/engine/install/ubuntu/) or `brew install --cask docker` on Mac
* **[uv](https://github.com/astral-sh/uv)** (Python package manager)
* **[Ollama](https://ollama.com/download)** installed & running locally

---

## 📂 2. Project Structure

```
document-chatbot/
├── app/
│   ├── ingest.py         # PDF/TXT → chunks → embeddings
│   ├── search.py         # Retrieve from FAISS + PostgreSQL
│   ├── rag_chain.py      # RAG logic (Ollama → OpenAI fallback)
│   ├── ui.py             # Streamlit chat interface
│   └── db_migration.py   # Create/drop tables
├── data/raw/             # Store your documents here
├── models/faiss_index/   # Persisted FAISS index file
├── init.sh               # Wait for Postgres & run migrations
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚡ 3. Installation

**1️⃣ Clone the repo**

```bash
git clone https://github.com/yourname/document-chatbot.git
cd document-chatbot
```

**2️⃣ Create & activate virtual environment**

```bash
uv venv venv
source venv/bin/activate
```

**3️⃣ Install dependencies**

```bash
uv pip install -r requirements.txt
```

---

## 🦙 4. Install & Run Ollama

Start Ollama:

```bash
ollama serve
```

Pull a model (example: llama3):

```bash
ollama pull llama3
```

Test it:

```bash
ollama run llama3 "Hello!"
```

---

## ⚙ 5. Configure Environment

Create `config.env`:

```env
PG_HOST=localhost
PG_USER=chatbot
PG_PASSWORD=chatbot
PG_DATABASE=chatbot_db
PG_PORT=5432

OLLAMA_HOST="http://localhost:11434"
OLLAMA_MODEL="llama3"
OPENAI_API_KEY="your-openai-key"
```

---

## 🐳 6. Start PostgreSQL with Docker

```bash
docker-compose --env-file config.env up -d
```

Run database migrations:

```bash
python3 app/db_migration.py up
```

---

## 📄 7. Prepare Documents

Put your PDFs/TXT files in:

```
data/raw/
```

Example:

```
data/raw/aws_rag_guide.pdf
```

---

## 🔍 8. Ingest Documents

```bash
python3 app/ingest.py
```

This will:

* Read docs
* Chunk text
* Create embeddings
* Store in FAISS + PostgreSQL

---

## 💬 9. Launch the Chatbot

```bash
streamlit run app/ui.py --server.port=8501
```

Open: [http://localhost:8501](http://localhost:8501)

---

Do you want me to also add **a “Quick Start with Docker” section** so beginners can run the entire stack (Postgres + chatbot UI) without installing Python locally? That would make the repo very plug-and-play.


## 🛠 10. Troubleshooting

* **Ollama not running?** → Run `ollama serve` before starting Streamlit.
* **Model not found?** → Run `ollama pull llama3` (or whichever model you want).
* **Slow responses?** → Try a smaller model like `mistral` instead of `llama3`.

---

## 📜 Example curl to Ollama

If you want to send requests manually:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Explain RAG in simple words"
}'
```
