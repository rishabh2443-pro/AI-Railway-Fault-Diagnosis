import requests
import psycopg2
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ==============================
# PostgreSQL Configuration
# ==============================

DB_CONFIG = {
    "host": "localhost",
    "database": "railway_monitoring",
    "user": "postgres",
    "password": "123@abesec",
    "port": "5432"
}


# ==============================
# Ollama Configuration
# ==============================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


# ==============================
# Build RAG Knowledge Index
# ==============================

def build_knowledge_index():

    knowledge_file = Path("knowledge/railway_faults.txt")

    text = knowledge_file.read_text(encoding="utf-8")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(embeddings).astype("float32")
    )

    return model, index, chunks


# ==============================
# Retrieve Relevant Knowledge
# ==============================

def retrieve_knowledge(query, model, index, chunks):

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        k=2
    )

    relevant_knowledge = []

    for i in indices[0]:
        relevant_knowledge.append(chunks[i])

    return "\n\n".join(relevant_knowledge)


# ==============================
# Get Latest Fault
# ==============================

def get_latest_fault():

    conn = psycopg2.connect(**DB_CONFIG)

    cursor = conn.cursor()

    query = """
    SELECT train_id, faults, risk
    FROM fault_results
    ORDER BY id DESC
    LIMIT 1;
    """

    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# ==============================
# Ollama AI Diagnosis
# ==============================

def get_ai_diagnosis(
    train_id,
    fault,
    risk,
    knowledge
):

    prompt = f"""
You are an AI railway fault diagnosis assistant.

Train ID:
{train_id}

Detected Fault:
{fault}

Risk Level:
{risk}

Relevant Railway Maintenance Knowledge:
{knowledge}

Using the detected fault and the provided maintenance knowledge,
generate a practical diagnosis.

Provide:

1. Diagnosis
2. Possible Cause
3. Recommended Action
4. Safety Advice

Keep the answer concise and practical.

Do not invent sensor values.
Use the provided railway knowledge as the main reference.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:

        return response.json()["response"]

    return "❌ Ollama connection failed."


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("\n🔄 Loading RAG knowledge base...")

    model, index, chunks = build_knowledge_index()

    print("✅ RAG knowledge index ready!")

    result = get_latest_fault()

    if result:

        train_id, fault, risk = result

        print("\n==============================")
        print("🚆 LATEST RAILWAY FAULT")
        print("==============================")

        print("Train ID:", train_id)
        print("Fault:", fault)
        print("Risk:", risk)

        print("\n🔎 Searching railway knowledge...")

        knowledge = retrieve_knowledge(
            fault,
            model,
            index,
            chunks
        )

        print("✅ Relevant knowledge retrieved!")

        print("\n🤖 Generating AI diagnosis...")

        diagnosis = get_ai_diagnosis(
            train_id,
            fault,
            risk,
            knowledge
        )

        print("\n==============================")
        print("🤖 AI RAILWAY DIAGNOSIS")
        print("==============================")

        print(diagnosis)

    else:

        print("❌ No fault data found in database.")