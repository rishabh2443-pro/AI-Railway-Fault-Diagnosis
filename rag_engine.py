from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# ==============================
# 1. Knowledge file load karo
# ==============================

knowledge_file = Path("knowledge/railway_faults.txt")

text = knowledge_file.read_text(encoding="utf-8")


# ==============================
# 2. Text ko chunks mein divide karo
# ==============================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(text)

print("✅ Knowledge base loaded!")
print("Total chunks:", len(chunks))


# ==============================
# 3. Embedding model load karo
# ==============================

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("✅ Embedding model loaded!")


# ==============================
# 4. Knowledge chunks ke embeddings
# ==============================

embeddings = model.encode(chunks)

print("✅ Embeddings created!")
print("Embedding shape:", embeddings.shape)


# ==============================
# 5. FAISS vector database
# ==============================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings).astype("float32"))

print("✅ FAISS index created!")
print("Total vectors:", index.ntotal)


# ==============================
# 6. Test Search
# ==============================

query = "What should I do if train vibration is very high?"

query_embedding = model.encode([query])

distances, indices = index.search(
    np.array(query_embedding).astype("float32"),
    k=2
)


# ==============================
# 7. Show relevant knowledge
# ==============================

print("\n🔎 Query:")
print(query)

print("\n--- Relevant Knowledge ---")

for i in indices[0]:
    print("\n", chunks[i])