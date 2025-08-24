import json
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import requests

load_dotenv()

api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DALLE_DEPLOYMENT")  # e.g., "dall-e"

prompt = 'A futuristic cat dwelling in the sunset, highly detailed, digital art.'

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-05-01-preview"
)

response = client.images.generate(
    model=deployment_name,
    prompt=prompt,
    n=1, # Number of images
    size= "1024*1024",
    quality='standard'
)

image_url = response.data[0].url

image_data = requests.get(image_url).content

with open('img.png', 'w') as file:
    file.write(image_data)


