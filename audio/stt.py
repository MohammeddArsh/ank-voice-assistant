from faster_whisper import WhisperModel
from config import WHISPER_MODEL

# Load model once at startup (downloads on first run, cached after)
print(f"⏳  Loading Whisper '{WHISPER_MODEL}' model...")
model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
print("✅  Whisper ready.")


def transcribe(audio_filepath: str) -> str:
    """
    Transcribes a .wav file using local faster-whisper.
    No internet or API key needed.
    """
    segments, _ = model.transcribe(audio_filepath, language="en")
    text = " ".join(segment.text for segment in segments).strip()
    print(f"📝  You said: \"{text}\"")
    return text
