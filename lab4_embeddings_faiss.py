"""
Lab 4 - Generate and Use Embeddings (with FAISS)
---------------------------------------------------
This script demonstrates:
1. Using Azure OpenAI to generate embeddings for text.
2. Storing embeddings in a local FAISS vector store.
3. Performing a semantic similarity search.

Why this matters:
- Embeddings convert text into numerical vectors.
- Similar vectors represent semantically similar text.
- This is the foundation for RAG (Retrieval Augmented Generation).

Cost tip:
- Using 'text-embedding-ada-002' is cheap ($0.0001 per 1K tokens).
"""

import os
import faiss
import numpy as np
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load credentials
load_dotenv()

api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_EMBEDDING")  # e.g., "text-embedding-ada-002"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview"
)

def get_embedding(text):
    """Generate embedding for given text using Azure OpenAI."""
    response = client.embeddings.create(
        model=deployment_name,
        input=text
    )

    return response.data[0].embedding

# ---- Sample dataset ----
documents = [
    "Azure OpenAI provides GPT models for natural language processing.",
    "Azure Cognitive Services has prebuilt APIs for vision, speech, and language.",
    "Azure Machine Learning lets you build and train custom ML models.",
    "Microsoft Azure provides cloud infrastructure services like VMs and storage."
]

# Create embeddings for dataset
embeddings = [get_embedding(docs) for docs in documents]
dimensions = len(embeddings[0])

# Convert to numpy array
embeddings_np = np.array(embeddings).astype('float32')

# ---- Build FAISS index ----
index = faiss.IndexFlatL2(dimensions)   # L2 distance
index.add(embeddings_np)

print(f"Stored {index.ntotal} documents in FAISS index.")

# ---- Perform a similarity search ----
query = "Which Azure service helps with AI-powered text analysis?"
query_embedding = np.array([get_embedding(query)]).astype('float32')

# Search top 2 similar docs
distances, indices = index.search(query_embedding, k=2)

print("\n=== Query ===")
print(query)

print("\n=== Top Results ===")
for idx, dist in zip(indices[0], distances[0]):
    print(f"Doc: {documents[idx]} (Distance: {dist:.4f})")

