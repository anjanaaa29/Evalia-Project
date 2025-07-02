import whisper
import io
import wave
from streamlit_mic_recorder import mic_recorder
import streamlit as st

class VoiceProcessor:
    def __init__(self, model="base"):
        """Load Whisper model (tiny, base, small, medium, large)"""
        self.model = whisper.load_model(model)
        self.silence_duration = 3.0

    def _get_wav_sample_rate(self, audio_bytes):
        """Detects sample rate from WAV header"""
        with io.BytesIO(audio_bytes) as wav_file:
            with wave.open(wav_file, 'rb') as wav:
                return wav.getframerate()

    def record_audio(self, key_suffix=""):
        """Record audio with automatic sample rate detection"""
        audio = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            format="wav",
            key=f"recorder_{key_suffix}"
        )
        if audio and audio['bytes']:
            sample_rate = self._get_wav_sample_rate(audio['bytes'])
            return {
                'bytes': audio['bytes'],
                'sample_rate': sample_rate
            }
        return None

    def transcribe_audio(self, audio_data):
        """Transcribe audio using local Whisper model"""
        try:
            if not audio_data:
                return ""
            
            # Save to a temporary file (Whisper needs a file path)
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_data['bytes'])
            
            # Transcribe
            result = self.model.transcribe("temp_audio.wav")
            return result["text"].strip()
        
        except Exception as e:
            st.error(f"Transcription error: {e}")
            return ""
