🧑‍🏫 Meet 1: Introduction to LLMs & RAG
**What is a chatbot? What’s different with LLMs?**

Yes, **chatbots** and **LLMs (Large Language Models)** are related but **not the same thing**. Here’s a clear breakdown:

## 🤖 **Chatbot**

* **Definition**: A software application designed to interact with users in a conversational manner.
* **Purpose**: Solve a specific use case (answer FAQs, customer support, booking, tutoring).
* **Behavior**:

  * Often **task-focused**.
  * May have **rule-based logic**, e.g., predefined scripts or decision trees.
  * Can also integrate **LLMs** for more natural conversations.
* **Examples**:

  * Customer support bot on Tokopedia or Shopee.
  * Banking chatbot that only knows about account balance & transactions.
  * Your **AWS RAG chatbot** (it’s a chatbot powered by an LLM + vector DB).

---

## 🧠 **LLM (Large Language Model)**

* **Definition**: An AI model trained on massive amounts of text to **predict and generate human-like language**.
* **Purpose**: General-purpose reasoning, text generation, and understanding.
* **Behavior**:

  * Doesn’t inherently know your business rules or database.
  * Needs to be **guided by prompts** or **connected to a knowledge base** (like RAG).
* **Examples**:

  * GPT‑4, LLaMA 3, Mistral, Gemini 1.5.
  * They can answer a wide range of questions but are not focused unless you constrain them.

---

## 🔗 **Relationship**

* A **chatbot** is the **application**.
* An **LLM** can be the **engine behind the chatbot**, making it smarter and more conversational.
* Without an LLM, a chatbot is usually **rule-based**.
* With an LLM (and optionally RAG), the chatbot can **understand and generate answers dynamically**.


**What is Retrieval-Augmented Generation (RAG)?**

RAG stands for **Retrieval-Augmented Generation**.
It’s a popular technique for **making LLMs answer accurately using external knowledge**.

---

## 🔹 Why RAG Exists

* **Problem with LLMs**:
  LLMs like GPT-4 or LLaMA **don’t know your private data** and may **hallucinate** (make up answers).
* **Solution**:
  Instead of relying only on the model’s memory, **RAG retrieves relevant documents first**, then **feeds them into the LLM** to ground its answer.

---

## 🔹 How RAG Works

1. **Retrieval Phase**

   * Split your knowledge base (PDFs, web pages, manuals) into chunks.
   * Embed them into a **vector database** (like FAISS, Pinecone, or Weaviate).
   * When a user asks a question, retrieve **top‑k relevant chunks**.

2. **Augmented Generation Phase**

   * Combine the retrieved context with the user’s question.
   * Send that **context + question** as a prompt to the LLM.
   * LLM generates a **grounded answer** using the retrieved documents.

---

### 🔹 Simple Flow

```
User Question
     ↓
Vector Search in Knowledge Base (Retrieval)
     ↓
Top-k Relevant Chunks
     ↓
Combine with Prompt → Send to LLM (Generation)
     ↓
Answer (Grounded in Real Docs)
```

---

### 🔹 Benefits of RAG

* ✅ Reduces hallucination.
* ✅ No need to fine‑tune the LLM.
* ✅ Updates easily: just update the knowledge base.
* ✅ Keeps private/company data **out of LLM training**.

---

In your **AWS chatbot course**, RAG is exactly what we’re doing:

* Storing AWS docs in FAISS (retrieval)
* Passing top‑chunks to LLaMA/OpenAI (generation)


**Use cases of chatbots for docs.**

**Overview of the tools we’ll use.**

📘 Assignment: Explore https://docs.aws.amazon.com/ and choose a service (e.g., EC2 or Lambda).

- uv : [installation](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
- Python via uv [installation](https://docs.astral.sh/uv/guides/install-python/)
- ollama: https://ollama.com/: curl -fsSL https://ollama.com/install.sh | sh

- Install python environment : `uv venv document-chatbot-venv`
- acivate: `source document-chatbot-venv/bin/activate`
```
ollama serve
ollama pull llama3
# take quite long time to pull image around 16m28s
```

- uv pip install requests
