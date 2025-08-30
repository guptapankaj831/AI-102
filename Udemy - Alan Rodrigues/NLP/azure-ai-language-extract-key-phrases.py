import os
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv('LANGUAGE_SERVICE_ENDPOINT')
key = os.getenv('LANGUAGE_SERVICE_KEY')

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [
'Machine Learning (ML) is a subset of Artificial Intelligence (AI) that enables systems to learn from data and improve over time without being explicitly programmed.',
'AI encompasses broader techniques that allow machines to mimic human intelligence, including reasoning, learning, and problem-solving.'
]

response = client.extract_key_phrases(
    documents=documents
)

print(response)

for res in response:
    for key_phrase in res.key_phrases:
        print(key_phrase)
