import os
from dotenv import load_dotenv

import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_endpoint = os.getenv('SPEECH_SERVICE_ENDPOINT')
speech_key = os.getenv('SPEECH_SERVICE_KEY')

from_language = 'en-US'
to_language = ['hi', 'fr'] # Hindi and French

translate_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, endpoint=speech_endpoint)
translate_config.speech_recognition_language = from_language

for lang in to_language:
    translate_config.add_target_language(lang)

audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

translator = speechsdk.translation.TranslationRecognizer(translation_config=translate_config, audio_config=audio_config)

result = translator.recognize_once_async().get()

if result.reason == speechsdk.ResultReason.TranslatedSpeech:
    print(result.text)

