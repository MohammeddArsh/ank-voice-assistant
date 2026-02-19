import sounddevice as sd
from scipy.io.wavfile import write
import os
import uuid
from config import SAMPLE_RATE, RECORD_SECONDS, CHANNELS


def record_audio() -> str:
    print(f"Listening for {RECORD_SECONDS} seconds... speak now!")

    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    )
    sd.wait()
    print("Got it.")

    tmp_path = os.path.join(os.path.expanduser("~"), "rec_" + uuid.uuid4().hex + ".wav")
    write(tmp_path, SAMPLE_RATE, audio)
    return tmp_path


def cleanup(filepath: str):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass
