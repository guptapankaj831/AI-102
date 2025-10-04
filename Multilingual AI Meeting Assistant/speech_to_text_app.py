"""
speech_to_text_app.py

Module 1: (Speech → Text) for Multilingual AI Meeting Assistant (optional Speaker Diarization)

Features:
- Upload audio (.wav, .mp3, .amr etc. via pydub/ffmpeg)
- Convert AMR input to WAV if required
- Optional Speaker Diarization (ConversationTranscriber)
- Displays the transcript in a Streamlit web app.

Usage:
  - Install requirements:
      pip install azure-cognitiveservices-speech streamlit pydub
  - Also ensure ffmpeg is installed on system PATH for pydub to handle AMR/MP3/etc.
  - Azure Services: Speech Service

Author: Pankaj Gupta
"""

import os
import azure.cognitiveservices.speech as speechsdk
import streamlit as st
import traceback
from dotenv import load_dotenv
from pydub import AudioSegment  # for audio conversion
import threading

# ==============================
# CONFIGURATION
# ==============================
load_dotenv()

AZURE_SPEECH_KEY = os.getenv("SPEECH_SERVICE_KEY")
AZURE_SPEECH_ENDPOINT = os.getenv("SPEECH_SERVICE_ENDPOINT")

def get_audio_duration(file_path: str) -> float:
    """Return audio duration in seconds."""
    audio = AudioSegment.from_file(file_path)
    return len(audio) / 1000.0  # pydub gives ms

def convert_to_wav(input_path: str) -> str:
    """
    Convert input audio file (.amr, .mp3, etc.) into .wav format for Azure Speech.

    Args:
        input_path (str): Path to uploaded file.

    Returns:
        str: Path to converted .wav file.
    """
    output_path = input_path.rsplit(".", 1)[0] + "_converted.wav"

    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format='wav')
        return output_path
    except Exception as e:
        raise RuntimeError(f"Failed to convert file: {e}")

def transcribe_audio(file_path: str, language: str = "en-US") -> str:
    """
    Transcribe audio into text using Azure Speech continuous recognition.
    Supports multiple languages.
    Shows live transcript + progress bar in Streamlit.

    Args:
        file_path (str): Path to the audio file.
        language (str): Language of audio file.

    Returns:
        str: Transcribed text from the audio.
    """
    try:
        total_duration = get_audio_duration(file_path)

        # Configure Azure Speech recognizer
        speech_config = speechsdk.SpeechConfig(endpoint=AZURE_SPEECH_ENDPOINT, subscription=AZURE_SPEECH_KEY)
        speech_config.speech_recognition_language = language

        audio_input = speechsdk.audio.AudioConfig(filename=file_path)

        # Azure Speech recognizer
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_input
        )

        transcript_parts = []
        done_event = threading.Event()

        # Streamlit progress UI
        live_output = st.empty()
        live_output.info("🎤 Listening and transcribing... Please wait.")
        progress_bar = st.progress(0, text="Processing audio...")

        # Collect recognized speech
        def recognized_handler(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                transcript_parts.append(evt.result.text)

                # Show partial transcript in real time
                live_output.write(" ".join(transcript_parts))

                # Estimate progress from result offset
                if evt.result.offset and evt.result.duration:
                    elapsed_sec = (evt.result.offset + evt.result.duration) / 10_000_000
                    progress = min(int((elapsed_sec / total_duration) * 100), 100)
                    progress_bar.progress(progress, text=f"⏳ Processing {progress}%")

        # Stop recognition when session ends or gets canceled
        def stop_cb(evt):
            done_event.set()

        # Attach handler
        speech_recognizer.recognized.connect(recognized_handler)
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start recognition & wait until finished
        speech_recognizer.start_continuous_recognition()
        done_event.wait()
        speech_recognizer.stop_continuous_recognition()

        # Clear progress and return final transcript
        progress_bar.progress(100, text="✅ Done")
        live_output.empty() #success("✅ Transcription finished")
        return " ".join(transcript_parts).strip() or "❌ No speech recognized."
    except Exception as e:
        print(traceback.format_exc())
        return f"Error during transcription: {str(e)}"


# ---------------- Speaker Diarization (multi-speaker) ----------------
def diarize_audio(file_path: str, language: str = "en-US", auto_speaker_count: bool = True, speaker_count: int | None = None) -> list[dict]:
    """
    Perform speaker diarization using ConversationTranscriber.
    Returns list of {"speaker": <id>, "text": <segment>, "offset": <sec>, "duration": <sec>}
    Uses threading.Event to wait for completion.
    Note: ConversationTranscriber & SpeakerDiarizationConfig availability depends on SDK version.
    """
    total_duration = get_audio_duration(file_path)

    speech_config = speechsdk.speech.SpeechConfig(endpoint=AZURE_SPEECH_ENDPOINT, subscription=AZURE_SPEECH_KEY)
    speech_config.speech_recognition_language = language

    audio_config = speechsdk.audio.AudioConfig(filename=file_path)

    try:
        # Ask service to include intermediate diarization info in transcribing events.
        # This helps to get speaker id in `transcribing` events.
        speech_config.set_property(
            property_id=speechsdk.PropertyId.SpeechServiceResponse_DiarizeIntermediateResults, 
            value=True
        )
    except Exception:
        pass

    transcriber = speechsdk.transcription.ConversationTranscriber(
        speech_config=speech_config, audio_config=audio_config
    )



# ==============================
# STREAMLIT UI
# ==============================
def main():
    """
        Streamlit App: Upload an audio file and transcribe it.
    """

    st.set_page_config(page_title="🌍 Multilingual Meeting Assistant", layout="centered")
    st.title('Multilingual Meeting Assistant')
    st.write('Upload a `.wav`, `.mp3`, or `.amr` file and transcribe speech to text in multiple languages.')

    # Language selector
    lang_choice = st.selectbox(
        "Select transcription language",
        options=["en-US", "hi-IN", "es-ES", "fr-FR", "de-DE", "zh-CN"]
    )

    uploaded_file = st.file_uploader('Uploaded Audio', type=['wav', 'mp3', 'amr'])

    if uploaded_file is not None:
        # Save uploaded file temporarily
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Convert .amr → .wav before transcription
        if uploaded_file.name.endswith(".amr"):
            amr_to_wav = st.empty()
            amr_to_wav.info("Converting .amr to .wav for compatibility...")
            temp_file_path = convert_to_wav(temp_file_path)
            amr_to_wav.empty()

        st.audio(temp_file_path)
        if st.button("Transcribe"):
            transcribing_audio = st.empty()
            transcribing_audio.info("Transcribing audio, please wait...")
            transcript = transcribe_audio(temp_file_path, language=lang_choice)
            transcribing_audio.empty()

            st.success('Transcription complete')
            st.text_area("Transcript", transcript, height=200)

        # Cleanup
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()
