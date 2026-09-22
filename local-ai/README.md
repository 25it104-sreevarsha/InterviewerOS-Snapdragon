# Local AI Service (Snapdragon On-Device Path)

This service replaces the cloud-based speech processing in Interviewer OS
with a fully local, offline pipeline, so no audio ever leaves the device.

## What it does
- Runs OpenAI Whisper (via faster-whisper) locally to transcribe interview
  answers, instead of sending audio to a cloud API.
- Exposes a simple REST API (`/transcribe`, `/health`) that the main
  Interviewer OS backend calls instead of its cloud speech provider.

## Snapdragon deployment path
This service is built on ONNX Runtime, which supports Qualcomm's QNN
execution provider. On a Snapdragon-powered HP PC, the Whisper model is
exported to ONNX and run on the NPU via QNN instead of CPU, giving faster,
lower-power, fully offline transcription. Model export and profiling for
this step use Qualcomm AI Hub.

## Running it
\`\`\`
cd local-ai
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn faster-whisper python-multipart
uvicorn server:app --port 8001
\`\`\`

## Status
- CPU-based local transcription: working (this repo)
- NPU-accelerated transcription via QNN: documented deployment path,
  pending access to Snapdragon hardware for on-device benchmarking