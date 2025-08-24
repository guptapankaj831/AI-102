from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("AZURE_CONTENTSAFETY_KEY")
endpoint = os.getenv("AZURE_CONTENTSAFETY_ENDPOINT")

client = ContentSafetyClient(endpoint, AzureKeyCredential(api_key))

query = input("Please enter your question:")
text = AnalyzeTextOptions(text=query)
response = client.analyze_text(text)
print(response)

# # Below will be the output. Severity will be different based on image.
# {
#     'blocklistsMatch': [],
#     'categoriesAnalysis': [
#         {
#             'category': 'Hate',
#             'severity': 0,
#         },
#         {
#             'category': 'SelfHarm',
#             'severity': 0,
#         },
#         {
#             'category': 'Sexual',
#             'severity': 0,
#         },
#         {
#             'category': 'Violence',
#             'severity': 0,
#         }
#     ]
# }
