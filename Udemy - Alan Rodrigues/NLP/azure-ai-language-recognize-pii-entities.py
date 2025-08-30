import os
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv('LANGUAGE_SERVICE_ENDPOINT')
key = os.getenv('LANGUAGE_SERVICE_KEY')

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [
"Sundar Pichai announced 1st quarter result from Google Head office California.",
]

response = client.recognize_pii_entities(
    documents=documents
)

print(response)

for result in response:
    for entities in result.entities:
        print(f"Category: {entities.category}, Confidence: {entities.category}, Text: {entities.text}")
