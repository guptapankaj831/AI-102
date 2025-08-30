import os
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv('LANGUAGE_SERVICE_ENDPOINT')
key = os.getenv('LANGUAGE_SERVICE_KEY')

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [
"Chaga is not a good resturant. They don't have good food.",
"This product is not good. I want my refund"
]

response = client.analyze_sentiment(
    documents=documents
)

print(response)

for result in response:
    print(f"Sentiment: {result.sentences[0].sentiment}, Text: {result.sentences[0].text}")
