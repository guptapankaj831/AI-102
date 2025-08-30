import os
from dotenv import load_dotenv

import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_endpoint = os.getenv('SPEECH_SERVICE_ENDPOINT')
speech_key = os.getenv('SPEECH_SERVICE_KEY')

config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=speech_endpoint)

output_file = 'transcribed.txt'
audio_file_name = 'speech01.wav'
config.speech_recognition_language='en-US'

# Use to take input from direct microphone
# audio_input = speechsdk.audio.AudioConfig(use_default_microphone=True)

audio_input = speechsdk.audio.AudioConfig(filename=audio_file_name)
text_generator = speechsdk.SpeechRecognizer(speech_config=config, audio_config=audio_input)
result = text_generator.recognize_once_async().get()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    with open(output_file, 'w') as output:
        output.write(result.text)
