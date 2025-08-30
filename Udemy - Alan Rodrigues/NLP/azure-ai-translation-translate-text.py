import os
from dotenv import load_dotenv

from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential

load_dotenv()

endpoint = os.getenv('TRANSLATION_ENDPOINT')
key = os.getenv('TRANSLATION_KEY')

client = TextTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))

source = 'en'
target = ['it', 'fr', 'hi', 'en']

documents = [
    InputTextItem(text="I am not feeling well."),
    InputTextItem(text='नमस्ते, आप कैसे हैं')
]

response = client.translate(documents, to_language=target)

print(response)

for item in response:
    if item.detected_language:
        print(f"Language: {item.detected_language.language}, Score: {item.detected_language.score}")
    
    for t in item.translations:
        print(f"Translated To: {t.to}, Translated Text: {t.text}")
