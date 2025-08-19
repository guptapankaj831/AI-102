"""
Lab 2 - Call Chat Completions with Parameters
------------------------------------------------
This script demonstrates how to:
1. Send chat completion requests to Azure OpenAI.
2. Use system, user, and assistant roles in the conversation.
3. Adjust key parameters (temperature, max_tokens, top_p).
4. Compare outputs with different parameter settings.

Keep in mind:
- Temperature controls creativity (0 = deterministic, 1 = creative).
- Max_tokens limits length of output.
- top_p controls probability distribution of token sampling.
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g., "gpt35"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview"
)

# Function to send a chat request
def ask_model(question, temperature=0.7, max_tokens=100, top_p=1.0):
    """Send a prompt to Azure OpenAI and return response text."""
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {'role': 'system', 'content': 'You are a concise assistant.'},
            {'role': 'user', 'content': question}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p
    )

    return response.choices[0].message.content

# Test different parameter settings
question = "Explain the difference between Azure Cognitive Services and Azure OpenAI."

print("=== Default Settings (temperature=0.7) ===")
print(ask_model(question))

print("\n=== Low Creativity (temperature=0) ===")
print(ask_model(question, temperature=0))

print("\n=== Very Creative (temperature=1) ===")
print(ask_model(question, temperature=1))

print("\n=== Short Answer (max_tokens=30) ===")
print(ask_model(question, max_tokens=30))

print("\n=== Controlled Diversity (top_p=0.5) ===")
print(ask_model(question, top_p=0.5))

