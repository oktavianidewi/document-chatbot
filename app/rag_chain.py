import os
import requests
import openai
from search import search
import json

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ask(query: str, top_k: int = 3) -> str:
    # 1️⃣ Get top-k chunks
    results = search(query, k=top_k)
    if not results:
        return "No relevant documents found."

    context = "\n".join(r["chunk"] for r in results)
    prompt = f"""
You are an AWS documentation assistant.
Use the following context to answer the question.
If the answer is not in the context, say you don"t know.

Context:
{context}

Question: {query}
Answer:
"""

    # 2️⃣ Try Ollama first
    # "prompt": prompt,

    try:

        payload = json.dumps({
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "timeout": 30,
            "stream": False
        })
        headers = {
            "Content-Type": "application/json"
        }

        url_path=f"{OLLAMA_HOST}/api/generate"

        response = requests.request(
            "POST", 
            url=url_path,
            headers=headers, 
            data=payload
        )
        # TODO: parse result

        data = response.json()
        # print(f"🔹 Ollama response: {data['response']}")
        if "response" in data and data["response"].strip():
            return data["response"].strip()
    except Exception as e:
        print(f"⚠️ Ollama error: {e}")

    # 3️⃣ Fallback to OpenAI if API key provided
    if OPENAI_API_KEY:
        openai.api_key = OPENAI_API_KEY
        completion = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AWS documentation assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0
        )
        return completion.choices[0].message["content"]

    return "[No response from model]"

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test RAG pipeline")
    parser.add_argument("query", help="Your question for the AWS chatbot")
    parser.add_argument("--k", type=int, default=3, help="Number of chunks to retrieve")
    args = parser.parse_args()

    print(f"🔹 Query: {args.query}")
    answer = ask(args.query, top_k=args.k)
    print("\n=== 🧠 RAG Answer ===")
    print(answer)