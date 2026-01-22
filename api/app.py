from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import base64
import io
import logging
import soundfile as sf
import numpy as np


from api.runpod_client import voice_to_voice_sync

# -------------------------
# Logging
# -------------------------
logging.basicConfig(level=logging.INFO)

# -------------------------
# Base directory (project root) for Vercel serverless
# -------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root

# -------------------------
# FastAPI app
# -------------------------
app = FastAPI()

# -------------------------
# Serve static files
# -------------------------
static_path = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_path):
    logging.warning(f"Static folder not found at {static_path}")
app.mount("/static", StaticFiles(directory=static_path), name="static")

# -------------------------
# Serve index.html
# -------------------------
index_file = os.path.join(static_path, "index.html")
@app.get("/")
async def index():
    if not os.path.exists(index_file):
        logging.error(f"index.html not found at {index_file}")
        return {"error": "index.html not found"}
    return FileResponse(index_file)

# -------------------------
# Request schema
# -------------------------
class AudioIn(BaseModel):
    audio_b64: str  # base64 from browser (webm/ogg)

# -------------------------
# Convert browser audio → WAV
# -------------------------
def convert_to_wav(audio_b64: str, sample_rate=16000) -> bytes:
    try:
        # Decode base64
        audio_bytes = base64.b64decode(audio_b64)
        audio_buffer = io.BytesIO(audio_bytes)

        # Read audio file with soundfile
        data, sr = sf.read(audio_buffer)

        # Convert to mono if needed
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        # Resample if sample_rate differs
        if sr != sample_rate:
            import resampy  # pip install resampy
            data = resampy.resample(data, sr, sample_rate)
            sr = sample_rate

        # Export WAV to bytes
        out = io.BytesIO()
        sf.write(out, data, sr, format='WAV')
        return out.getvalue()

    except Exception as e:
        logging.error(f"Error converting audio to WAV: {e}")
        raise RuntimeError("Audio conversion failed. Soundfile method failed.")

# -------------------------
# Voice-to-Voice API
# -------------------------
@app.post("/voice_to_voice")
async def voice_to_voice(data: AudioIn):
    try:
        # 1️⃣ Convert browser audio to WAV
        wav_bytes = convert_to_wav(data.audio_b64)
        wav_b64 = base64.b64encode(wav_bytes).decode("utf-8")

        # 2️⃣ Call RunPod API
        result = voice_to_voice_sync(wav_b64)

        if "audio_b64" not in result:
            logging.error(f"Invalid RunPod response: {result}")
            return {"error": "Voice processing failed"}

        return {
            "audio_b64": result["audio_b64"],
            "sample_rate": result.get("sample_rate", 24000),
            "transcription": result.get("transcription", ""),
            "llm_response": result.get("llm_response", "")
        }

    except Exception as e:
        logging.error(f"Voice-to-Voice error: {e}")
        return {"error": str(e)}
