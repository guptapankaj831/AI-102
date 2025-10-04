# Read or extract info from PDF or image using Azure document intelligence service.
# azure-ai-documentintelligence

from dotenv import load_dotenv
import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from azure.core.credentials import AzureKeyCredential

load_dotenv()

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT')
AZURE_DOCUMENT_INTELLIGENCE_KEY = os.getenv('AZURE_DOCUMENT_INTELLIGENCE_KEY')

client = DocumentIntelligenceClient(
    credential=AzureKeyCredential(AZURE_DOCUMENT_INTELLIGENCE_KEY), 
    endpoint=AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT
)

# Set analysis settings
fileUri = "https://github.com/MicrosoftLearning/mslearn-ai-information-extraction/blob/main/Labfiles/prebuilt-doc-intelligence/sample-invoice/sample-invoice.pdf?raw=true"
readModelId = "prebuilt-read"

response = client.begin_analyze_document(readModelId, AnalyzeDocumentRequest(url_source=fileUri))

result: AnalyzeResult = response.result()
print(result)

for res in result.styles:
    if res.is_handwritten:
        print(f"Handwritten text : confidence {res.confidence}")

for index, para in enumerate(result.paragraphs):
    print(f"Paragraph {index + 1}: {para.content}")



