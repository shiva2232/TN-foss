import tempfile
import wave
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice
import os
import config

def speak(text):
    # Load Piper voice model
    voice = PiperVoice.load(config.VOICE_DIR)  # Ensure this model exists

    # Create a temporary WAV file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        tmp_wav_path = tmp_wav.name

    # Synthesize speech directly into the WAV file
    with wave.open(tmp_wav_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit PCM
        wav_file.setframerate(voice.config.sample_rate)
        voice.synthesize_wav(text, wav_file=wav_file)

    # Read WAV file as NumPy array
    with wave.open(tmp_wav_path, 'rb') as wav_file:
        fs = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())
        audio_np = np.frombuffer(frames, dtype=np.int16)

    # Play audio
    sd.play(audio_np, samplerate=fs)
    sd.wait()

    # Delete temporary file
    os.remove(tmp_wav_path)

if __name__ == "__main__":
    speak("Hello world! This is Piper TTS speaking directly with your setup.")
