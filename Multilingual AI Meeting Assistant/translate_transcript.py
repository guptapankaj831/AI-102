"""
translate_transcript.py
-----------------------
Module 2 of Multilingual AI Meeting Assistant.
Translates meeting transcripts into multiple languages using Azure Translator API.

Translates meeting transcripts into multiple languages using Azure Translator SDK.

Requirements:
    pip install azure-ai-translation-text streamlit

Environment variables:
    AZURE_TRANSLATOR_KEY
    AZURE_TRANSLATOR_ENDPOINT
"""

import os
import streamlit as st
from dotenv import load_dotenv
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential

load_dotenv()

# Load credentials from environment
AZURE_TRANSLATOR_KEY = os.getenv("TRANSLATION_KEY")
AZURE_TRANSLATOR_ENDPOINT = os.getenv("TRANSLATION_ENDPOINT")


def translate_text(text: str, target_language: list, from_language: str='en-US') -> dict:
    """
        Translate text into multiple languages using Azure Translator.

        Args:
            text (str): Input text to translate.
            target_languages (list): List of target language codes (e.g. ["fr", "hi", "es"]).

        Returns:
            dict: Mapping of language code -> translated text
    """
    if not text.strip():
        return {"error": "❌ No text provided for translation."}

    input_text = [InputTextItem(text=text)]
    translate_client = TextTranslationClient(
        endpoint=AZURE_TRANSLATOR_ENDPOINT, 
        credential=AzureKeyCredential(AZURE_TRANSLATOR_KEY)
        )

    result = translate_client.translate(
        input_text, 
        to_language=target_language
#        from_language=from_language
    )

    translations = {}
    if result:
        for res in result[0].translations:
            translations[res.to] = res.text

    return translations


# ==============================
# STREAMLIT UI
# ==============================

def main():
    st.title('Multilingual AI Meeting Assistant')
    st.subheader('Translate Meeting Transcript')

    input_text = st.text_area("Enter transcript text:", "Hello everyone, welcome to our AI meeting!")
    target_lang = st.multiselect(
        "Select target language:",
        options=["fr", "es", "de", "hi", "zh-Hans"]
    )

    if st.button('Translate'):
        with st.spinner("Translating..."):
            translations = translate_text(input_text, target_lang)

            if 'error' in translations:
                st.error(translations['error'])
            else:
                for lang, translated_text in translations.items():
                    st.success(f"**{lang}:** {translated_text}")

            # Download option
            download_text = "\n".join([f"{lang}: {txt}" for lang, txt in translations.items()])
            st.download_button("📥 Download Translations", download_text, file_name="translations.txt")


if __name__ == '__main__':
    main()
