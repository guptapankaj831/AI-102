import os
from dotenv import load_dotenv

import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_endpoint = os.getenv('SPEECH_SERVICE_ENDPOINT')
speech_key = os.getenv('SPEECH_SERVICE_KEY')

config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=speech_endpoint)
config.speech_synthesis_voice_name = 'hi-IN-KavyaNeural'

input_text = 'Hello world, How are you.?'

output_file = 'speech02.wav'

audio_output = speechsdk.audio.AudioConfig(filename=output_file)

speech_generator = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=audio_output)

result = speech_generator.speak_text_async(input_text).get()
print(result)
