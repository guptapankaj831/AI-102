import os
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv('LANGUAGE_SERVICE_ENDPOINT')
key = os.getenv('LANGUAGE_SERVICE_KEY')

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [
    'Hello, how are you?',
    'नमस्ते, आप कैसे हैं?',
    'Bonjour, comment ça va ?'
]

response = client.detect_language(
    documents=documents
)

print(response)
