# No API keys needed — everything runs locally!

# Audio settings
SAMPLE_RATE = 16000      # Hz — Whisper works best at 16kHz
RECORD_SECONDS = 5       # How long to record each time you speak
CHANNELS = 1             # Mono audio

# Whisper settings (runs locally via faster-whisper)
WHISPER_MODEL = "base"   # Options: tiny, base, small, medium
                         # tiny = fastest, base = good balance, small/medium = more accurate

# LLM settings (runs locally via Ollama)
LLM_MODEL = "llama3.2"  # Must match what you pulled: `ollama pull llama3.2`
OLLAMA_URL = "http://localhost:11434"  # Default Ollama server address

SYSTEM_PROMPT = """You are a friendly, concise voice assistant. 
Keep your answers short and conversational — you're speaking out loud, not writing an essay.
Avoid bullet points or markdown formatting in your responses."""
