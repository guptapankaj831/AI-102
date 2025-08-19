"""
Lab 4B - Retrieval Augmented Generation (RAG) with FAISS
----------------------------------------------------------
This script demonstrates:
1. Generate embeddings for a small knowledge base.
2. Store them in a FAISS vector index (local, free).
3. Perform similarity search to find relevant documents.
4. Pass the retrieved documents as context to Azure OpenAI (GPT).
5. Get a grounded answer based only on the retrieved knowledge.

Why this matters:
- RAG ensures answers are based on your data, not just the model's memory.
- This is a core skill for AI-102.
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
embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING")  # e.g., "text-embedding-ada-002"
chat_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")      # e.g., "gpt35"

# Initialize client
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview"
)

def get_embedding(text):
    """Generate embedding for given text using Azure OpenAI."""
    response = client.embeddings.create(
        input=text,
        model=embedding_deployment
    )
    return response.data[0].embedding

def get_answer_with_context(question, docs):
    """Send a question + retrieved docs to GPT for grounded answer."""
    context_text = "\n".join(docs)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use only the provided context to answer."},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer strictly from the context."}
    ]

    response = client.chat.completions.create(
        model=chat_deployment,
        messages=messages,
        temperature=0.3,   # Lower temperature for more factual answers
        max_tokens=200
    )

    return response.choices[0].message.content

# ---- Knowledge Base ----
documents = [
    "Azure OpenAI provides GPT models for natural language processing.",
    "Azure Cognitive Services has prebuilt APIs for vision, speech, and language.",
    "Azure Machine Learning lets you build and train custom ML models.",
    "Microsoft Azure provides cloud infrastructure services like VMs and storage."
]

# Generate embeddings
embeddings = [get_embedding(docs) for docs in documents]
dimensions = len(embeddings[0])
embeddings_np = np.array(embeddings).astype('float32')

# Build FAISS index
index = faiss.IndexFlatL2(dimensions)
index.add(embeddings_np)

# ---- Query ----
query = "Which Azure service can I use to build my own machine learning model?"
query_embedding = np.array([get_embedding(query)]).astype('float32')

# Retrieve top 2 documents
distances, indices = index.search(query_embedding, k=2)
retrieved_docs = [documents[i] for i in indices[0]]

print("=== User Question ===")
print(query)

print("\n=== Retrieved Context ===")
for doc in retrieved_docs:
    print("-", doc)

# Get grounded answer from GPT
answer = get_answer_with_context(query, retrieved_docs)

print("\n=== GPT Answer (with RAG) ===")
print(answer)

