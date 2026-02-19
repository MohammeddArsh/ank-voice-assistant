# Ank — AI Voice Assistant

> A conversational AI assistant with a full speech interface, built with Python and a clean dark web UI.
> Speak naturally, get intelligent responses spoken back to you in real time.

![Ank Demo](docs/demo.png)
<!-- Take a screenshot of your UI and save it as docs/demo.png -->

---

## Overview

Ank is a full-stack voice assistant that combines speech recognition, large language model inference, and text-to-speech synthesis into a seamless conversational experience. Built to demonstrate end-to-end AI pipeline integration — from raw microphone audio to spoken AI responses — running entirely locally with no API costs.

**Live interaction flow:**

```
Your voice → Whisper (local) → Llama 3.2 (local) → gTTS → Spoken response
```

Everything runs on your machine. No cloud APIs, no costs, no data leaving your device.

---

## Features

- **Voice input** — Click the mic button or hold Spacebar to record
- **Real-time waveform** — Live symmetric audio visualizer while speaking
- **Conversational memory** — Remembers full session context across turns
- **Spoken responses** — Every reply converted to audio and played automatically
- **Chat history** — Full conversation displayed on screen with replay buttons
- **New Chat** — Resets session and conversation memory instantly
- **100% local** — Runs offline, no API keys required

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Browser (UI)                      │
│  MediaRecorder API → WAV blob → fetch(/chat)        │
│  ← JSON { user_text, reply, audio_url }             │
│  Audio() playback ← /audio/{file}                   │
└────────────────────┬────────────────────────────────┘
                     │ HTTP
┌────────────────────▼────────────────────────────────┐
│                FastAPI Backend                       │
│                                                      │
│  /chat endpoint                                      │
│    │                                                 │
│    ├── audio/stt.py      (faster-whisper → text)    │
│    ├── brain/memory.py   (append to history)        │
│    ├── brain/llm.py      (Ollama Llama 3.2 → reply) │
│    └── audio/tts.py      (gTTS → MP3 file)          │
│                                                      │
│  /audio/{file}  — serves generated MP3              │
│  /reset         — clears conversation memory        │
└─────────────────────────────────────────────────────┘
```

**Component breakdown:**

| Component | File | Responsibility |
|---|---|---|
| Web UI | `static/index.html` | Recording, waveform, chat display |
| API Server | `app.py` | Request routing, session management |
| Speech-to-Text | `audio/stt.py` | Transcribes audio using local Whisper model |
| LLM | `brain/llm.py` | Generates replies using Llama 3.2 via Ollama |
| Memory | `brain/memory.py` | Maintains multi-turn conversation history |
| Text-to-Speech | `audio/tts.py` | Converts reply text to MP3 via gTTS |

---

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Backend | Python 3.11, FastAPI, Uvicorn | Async REST API |
| Speech-to-Text | faster-whisper | Runs Whisper locally, no API key needed |
| LLM | Ollama + Llama 3.2 | Fully local inference, free forever |
| Text-to-Speech | gTTS + ffplay | Google TTS generation, ffplay for playback |
| Frontend | Vanilla HTML / CSS / JS | No framework, single file |
| Audio Capture | Web MediaRecorder API | Browser-native recording |

---

## Setup & Installation

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com) installed and running
- [ffmpeg](https://ffmpeg.org/download.html) installed

### 1. Clone the repository

```bash
git clone https://github.com/MohammeddArsh/ank-voice-assistant
cd ank-voice-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull the Llama model

```bash
ollama pull llama3.2
```

### 5. Configure ffmpeg path

Open `audio/tts.py` and update the path to match your ffmpeg installation:

```python
FFMPEG_DIR = r"C:\path\to\ffmpeg\bin"   # Windows
# FFMPEG_DIR = "/usr/local/bin"         # Mac / Linux
```

### 6. Run the server

```bash
uvicorn app:app --reload
```

### 7. Open in browser

```
http://localhost:8000
```

---

## Project Structure

```
ank-voice-assistant/
├── app.py                  # FastAPI server & API endpoints
├── config.py               # Model settings & constants
├── requirements.txt
├── static/
│   └── index.html          # Full web UI — single file
├── audio/
│   ├── capture.py          # Audio recording helper
│   ├── stt.py              # Speech-to-text via faster-whisper
│   └── tts.py              # Text-to-speech via gTTS
└── brain/
    ├── llm.py              # Llama 3.2 via Ollama
    └── memory.py           # Conversation history management
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web UI |
| `POST` | `/chat` | Accepts audio, returns transcript + reply + audio URL |
| `GET` | `/audio/{file}` | Serves generated TTS audio file |
| `POST` | `/reset` | Clears conversation memory |

---

## Built by

**Mohammed Arsh** — [github.com/MohammeddArsh](https://github.com/MohammeddArsh)
