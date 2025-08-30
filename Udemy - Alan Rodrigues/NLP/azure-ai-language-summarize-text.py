import os
from dotenv import load_dotenv

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv('LANGUAGE_SERVICE_ENDPOINT')
key = os.getenv('LANGUAGE_SERVICE_KEY')

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documents = [
    {'id': 1, 'text':"Artificial Intelligence (AI) enables machines to mimic human intelligence. It involves reasoning, problem-solving, and decision-making. AI powers applications like virtual assistants and smart robots. Machine Learning (ML) is a subset of AI focused on data-driven learning. ML models improve performance through experience without explicit programming."},
    {'id': 2, 'text':"ML and AI are transforming industries like healthcare, finance, and retail. AI uses algorithms to simulate cognitive functions such as perception. ML uses statistical techniques to find patterns in data. Supervised and unsupervised learning are common ML types. Their integration enables smarter automation and analytics."}
]

poller = client.begin_extract_summary(
    documents=documents
)
response = poller.result()
print(response)

for doc in response:
    if not doc.is_error:
        for sentense in doc.sentences:
            print(f"id: {doc.id}, Length: {sentense.length}, Rank: {sentense.rank_score}, Text: {sentense.text}")
