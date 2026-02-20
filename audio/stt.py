from config import MODE

if MODE == "openai":
    from audio.stt_openai import transcribe
else:
    from audio.stt_local import transcribe

__all__ = ["transcribe"]
