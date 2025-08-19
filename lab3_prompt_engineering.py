"""
Lab 3 - Prompt Engineering Patterns
------------------------------------------------
This script demonstrates:
1. Zero-shot prompting (no examples).
2. One-shot prompting (single example).
3. Few-shot prompting (multiple examples).
4. Using system message to control style and tone.

Prompt engineering helps guide the model to produce
better, more reliable, and context-appropriate outputs.
"""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Credentials
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g., "gpt35"

# Initialize client
client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version="2024-05-01-preview"
)

def run_prompt(messages, label):
    """Send a chat prompt and print response with a label."""
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )
    print(f"\n=== {label} ===")
    print(response.choices[0].message.content)


# 1. Zero-shot prompt
zero_shot = [
    {"role": "system", "content": "You are an assistant that explains concepts simply."},
    {"role": "user", "content": "Explain what Azure OpenAI Service is."}
]

# 2. One-shot prompt (with a single example)
one_shot = [
    {"role": "system", "content": "You are an assistant that gives short definitions."},
    {"role": "user", "content": "What is Azure Cognitive Services?"},
    {"role": "assistant", "content": "Azure Cognitive Services provides prebuilt AI APIs for vision, speech, language, and decision tasks."},
    {"role": "user", "content": "What is Azure OpenAI Service?"}
]

# 3. Few-shot prompt (with multiple examples)
few_shot = [
    {"role": "system", "content": "You are a helpful assistant that explains Azure services with examples."},
    {"role": "user", "content": "What is Azure Cognitive Services?"},
    {"role": "assistant", "content": "It’s a set of ready-to-use AI APIs. Example: Use Face API to detect faces in photos."},
    {"role": "user", "content": "What is Azure Machine Learning?"},
    {"role": "assistant", "content": "It’s a platform to build, train, and deploy ML models. Example: Train a churn prediction model."},
    {"role": "user", "content": "What is Azure OpenAI Service?"}
]

# Run all prompts
run_prompt(zero_shot, "Zero-Shot Prompt")
run_prompt(one_shot, "One-Shot Prompt")
run_prompt(few_shot, "Few-Shot Prompt")
