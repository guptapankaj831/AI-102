import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import requests

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

prompt = 'A futuristic cat dwelling in the sunset, highly detailed, digital art.'

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-05-01-preview"
)

# Initialize prompt with system message
prompt = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

# Add a user input message to the prompt
input_text = input("Enter a question: ")
prompt.append({"role": "user", "content": input_text})

# Additional parameters to apply RAG pattern using the AI Search index
rag_params = {
    'data_sources': [{
        'type': 'azure_search',
        'parameters': {
            'endpoint': 'AZURE_SEARCH_URL',
            'index_name': 'INDEX_NAME',
            'authentication': {
                'type': 'api_key',
                'key': 'AZURE_SEARCH_API_KEY'
            }
            # # Params for vector-based query
            # "query_type": "vector",
            # "embedding_dependency": {
            #     "type": "deployment_name",
            #     "deployment_name": "<embedding_model_deployment_name>",
            # },
        }
    }]
}

# Submit the prompt with the index information
response = client.chat.completions.create(
    model="deployment_name",
    messages=prompt,
    extra_body=rag_params
)

# Print the contextualized response
completion = response.choices[0].message.content
print(completion)

