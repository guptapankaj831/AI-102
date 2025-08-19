"""
Lab 1 - Setup & Test Azure OpenAI Deployment
------------------------------------------------
This script demonstrates how to connect to Azure OpenAI,
send a simple chat completion request, and print the response.

Steps covered:
1. Load API credentials from environment (.env file).
2. Initialize Azure OpenAI client with endpoint + key.
3. Send a sample prompt to the deployed model (gpt-35-turbo).
4. Print the model's response.

Keep in mind:
- Replace values in .env with your own Azure OpenAI details.
- Using gpt-35-turbo keeps the cost very low.
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv


# Load API key and endpoint from .env file
load_dotenv()

# Get environment variables
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g., "gpt35"

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview"  # Latest stable API version
)

# Send a test request
respose = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is capital of india?"}
    ],
    max_tokens=50,
    temperature=.7
)

# Print the response
print("=== Azure OpenAI Response ===")
print(respose.choices[0].message.content)

