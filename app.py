from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import sys

sys.path.insert(0, os.path.dirname(__file__))

from audio.stt import transcribe
from audio.tts import speak_to_file
from brain.llm import get_reply
from brain.memory import ConversationMemory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

memory = ConversationMemory()


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/chat")
async def chat(audio: UploadFile = File(...)):
    # Save uploaded audio
    audio_path = os.path.join(os.path.expanduser("~"), "upload_" + uuid.uuid4().hex + ".wav")
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    # Transcribe
    user_text = transcribe(audio_path)
    try:
        os.remove(audio_path)
    except Exception:
        pass

    if not user_text:
        return JSONResponse({"error": "Could not transcribe audio"}, status_code=400)

    # Get LLM reply
    memory.add_user_message(user_text)
    memory.trim_if_needed()
    reply = get_reply(memory.get_messages())
    memory.add_assistant_message(reply)

    # Convert reply to audio file
    audio_out = speak_to_file(reply)

    return JSONResponse({
        "user_text": user_text,
        "reply": reply,
        "audio_url": "/audio/" + os.path.basename(audio_out)
    })


@app.get("/audio/{filename}")
def get_audio(filename: str):
    path = os.path.join(os.path.expanduser("~"), filename)
    return FileResponse(path, media_type="audio/mpeg")


@app.post("/reset")
def reset():
    memory.__init__()
    return {"status": "reset"}
