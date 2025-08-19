"""
Lab 5 - Retrieval Augmented Generation (RAG) with Azure Cognitive Search
------------------------------------------------------------------------
This script demonstrates:
1. Index a set of documents into Azure Cognitive Search.
2. Perform semantic search with embeddings.
3. Pass retrieved docs as context to Azure OpenAI GPT.
4. Get grounded answers (only from your indexed knowledge).

Why this matters:
- Azure Cognitive Search + OpenAI is the foundation of enterprise RAG.
- Cognitive Search handles indexing, filtering, and large-scale retrieval.
"""

import os
from openai import AzureOpenAI
import requests
from dotenv import load_dotenv
import json

# Load credentials
load_dotenv()

# Azure Cognitive Search config
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")  # e.g., "https://your-search-service.search.windows.net"
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")            # Admin key
SEARCH_INDEX = "lab5-knowledge"

# Azure OpenAI config
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
chat_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview"
)


# ---- Step 1: Upload Knowledge Base to Cognitive Search ----
def create_index():
    """Create a search index if not exists."""
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX}?api-version=2023-11-01"
    headers = {"Content-Type": "application/json", "api-key": SEARCH_KEY}

    schema = {
        "name": SEARCH_INDEX,
        "fields": [
            {"name": "id", "type": "Edm.String", "key": True},
            {"name": "content", "type": "Edm.String", "searchable": True}
        ]
    }

    response = requests.put(url, headers=headers, data=json.dumps(schema))
    if response.status_code in [200, 201]:
        print("✅ Index created or already exists.")
    else:
        print("⚠️ Index creation issue:", response.text)


def upload_documents():
    """Upload documents to the search index."""
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX}/docs/index?api-version=2023-11-01"
    headers = {"Content-Type": "application/json", "api-key": SEARCH_KEY}

    documents = [
        {"id": "1", "content": "Azure OpenAI provides GPT models for natural language processing."},
        {"id": "2", "content": "Azure Cognitive Services has prebuilt APIs for vision, speech, and language."},
        {"id": "3", "content": "Azure Machine Learning lets you build and train custom ML models."},
        {"id": "4", "content": "Microsoft Azure provides cloud infrastructure services like VMs and storage."}
    ]

    payload = {"value": documents}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("✅ Documents uploaded successfully.")
    else:
        print("⚠️ Upload issue:", response.text)


# ---- Step 2: Query Cognitive Search ----
def search_documents(query):
    """Search for relevant docs in Azure Cognitive Search."""
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX}/docs/search?api-version=2023-11-01"
    headers = {"Content-Type": "application/json", "api-key": SEARCH_KEY}

    body = {
        "search": query,
        "queryType": "semantic",
        "semanticConfiguration": "default",
        "top": 2
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))
    result = response.json()
    return [doc['content'] for doc in result.get('value', [])]

# ---- Step 3: Pass retrieved docs to GPT ----
def get_answer_with_context(question, docs):
    """Send a question + retrieved docs to GPT for grounded answer."""
    context_text = "\n".join(docs)
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use only the provided context to answer."},
        {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {question}\nAnswer strictly from the context."}
    ]

    response = client.chat.completions.create(
        messages=messages,
        model=chat_deployment,
        temperature=0.3,
        max_tokens=200
    )

    return response.choices[0].message.content


# ---- Run the Lab ----
if __name__ == "__main__":
    # create_index()
    upload_documents()

    query = "Which Azure service helps me build my own ML model?"
    retrieved_docs = search_documents(query)

    print("=== User Question ===")
    print(query)

    print("\n=== Retrieved Context from Azure Cognitive Search ===")
    for doc in retrieved_docs:
        print("-", doc)

    answer = get_answer_with_context(query, retrieved_docs)

    print("\n=== GPT Answer (with RAG) ===")
    print(answer)

