from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import tempfile, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# "base" runs well on CPU. On a Snapdragon NPU this swaps to an
# AI Hub-exported Whisper model via the QNN execution provider.
model = WhisperModel("base", device="cpu", compute_type="int8")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    segments, info = model.transcribe(tmp_path, beam_size=5)
    text = " ".join(seg.text for seg in segments).strip()
    os.remove(tmp_path)

    return {
        "text": text,
        "language": info.language,
        "duration_sec": info.duration,
    }

@app.get("/health")
async def health():
    return {"status": "ok", "provider": "local-whisper"}