import os
from dotenv import load_dotenv

load_dotenv()

# ── Switch between "local" and "openai" ──────────────────────────────────────
MODE = "openai"   # "local" = Ollama + faster-whisper | "openai" = GPT + Whisper API

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio settings
SAMPLE_RATE = 16000
RECORD_SECONDS = 5
CHANNELS = 1

# LLM settings
LLM_MODEL_OPENAI = "gpt-4o-mini"
LLM_MODEL_LOCAL  = "llama3.2"

# Whisper settings (local mode only)
WHISPER_MODEL = "base"

SYSTEM_PROMPT = """You are Ank, a friendly and concise voice assistant built by Mohammed Arsh.
Keep answers short and conversational — you are speaking out loud, not writing an essay.
Avoid bullet points or markdown formatting in your responses."""
