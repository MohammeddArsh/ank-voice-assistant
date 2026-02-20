from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import uuid
import time
import glob
import sys

sys.path.insert(0, os.path.dirname(__file__))

from audio.stt import transcribe
from audio.tts import speak_to_file
from brain.llm import get_reply
from brain.memory import ConversationMemory
from brain.logger import SessionLogger


def cleanup_temp_files():
    home = os.path.expanduser("~")
    patterns = ["tts_*.mp3", "upload_*.wav", "rec_*.wav"]
    removed = 0
    for pattern in patterns:
        for f in glob.glob(os.path.join(home, pattern)):
            try:
                os.remove(f)
                removed += 1
            except Exception:
                pass
    if removed:
        print(f"Cleaned up {removed} leftover temp files.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_temp_files()
    yield
    cleanup_temp_files()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

memory = ConversationMemory()
logger = SessionLogger()


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.post("/chat")
async def chat(audio: UploadFile = File(...)):
    audio_path = os.path.join(os.path.expanduser("~"), "upload_" + uuid.uuid4().hex + ".wav")
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    user_text = transcribe(audio_path)
    try:
        os.remove(audio_path)
    except Exception:
        pass

    if not user_text:
        return JSONResponse({"error": "Could not transcribe audio"}, status_code=400)

    memory.add_user_message(user_text)
    memory.trim_if_needed()

    start_time = time.time()
    reply, token_usage = get_reply(memory.get_messages())
    response_time_ms = (time.time() - start_time) * 1000

    memory.add_assistant_message(reply)
    logger.log_turn(user_text, reply, response_time_ms, token_usage)

    audio_out = speak_to_file(reply)

    return JSONResponse({
        "user_text": user_text,
        "reply": reply,
        "audio_url": "/audio/" + os.path.basename(audio_out),
        "analytics": logger.get_analytics()
    })


@app.get("/audio/{filename}")
def get_audio(filename: str):
    path = os.path.join(os.path.expanduser("~"), filename)
    return FileResponse(path, media_type="audio/mpeg")


@app.post("/reset")
def reset():
    logger.reset()
    memory.__init__()
    cleanup_temp_files()
    return {"status": "reset"}


@app.get("/analytics")
def analytics():
    return logger.get_analytics()


@app.get("/export/json")
def export_json():
    data = logger.export_json()
    filename = f"ank_session_{logger.session_id}.json"
    return Response(
        content=data,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@app.get("/export/csv")
def export_csv():
    data = logger.export_csv()
    filename = f"ank_session_{logger.session_id}.csv"
    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


# Mount static LAST so it doesn't intercept API routes
app.mount("/static", StaticFiles(directory="static"), name="static")
