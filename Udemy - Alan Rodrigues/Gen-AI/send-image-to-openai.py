from openai import AzureOpenAI
import json
import os
from dotenv import load_dotenv
import base64

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")  # e.g., "gpt35"

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-05-01-preview"
)

with open('abc.png', 'rb') as image_file:
    image_detail = base64.b64encode(image_file.read()).decode('utf-8')

response = client.chat.completions.create(
    messages=[
        {
            'role': 'system',
            'content': 'You are helpfull assistant who helps to describe the images.'
        },
        {
            'role': 'user',
            'content': [
                {'type': 'text', 'text': 'Give me description of the what the image is trying to explain.'},
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': f'data:image/png;base64,{image_detail}'
                    }
                }
            ]
        }
    ],
    model=deployment_name,
    max_completion_tokens=1000    
)

print(response.choices[0].message.content)

#undumped_response = response.model_dump()
#print(json.dumps(undumped_response, indent=4))

