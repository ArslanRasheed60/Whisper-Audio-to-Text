from fastapi import FastAPI, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
import shutil
from fastapi.middleware.cors import CORSMiddleware
import whisper
import shutil
import os
import requests

from model import WhisperAudioURL


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the origins allowed here.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def test():
    return {"whisper":"working"}

@app.post("/transcribe-tiny/")
async def transcribe_audio_from_url(whisperAudioUrl: WhisperAudioURL):
    try:
        # Download the audio file from the provided URL
        response = requests.get(whisperAudioUrl.url, stream=True)
        if response.status_code == 200:
            with open("audio.mp3", "wb") as audio_file:
                shutil.copyfileobj(response.raw, audio_file)
            del response

            # Load the whisper model and transcribe the audio
            model = whisper.load_model("tiny")
            result = model.transcribe("audio.mp3")

            # Return the transcribed text
            item = {"detail": result["text"]}
            return JSONResponse(content=item, status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Failed to download audio file from the provided URL")
    except Exception as e:
        item = {"status": "failed", "message": str(e)}
        return JSONResponse(content=item, status_code=500)

@app.post("/transcribe-small/")
async def transcribe_audio_from_url(whisperAudioUrl: WhisperAudioURL):
    try:
        # Download the audio file from the provided URL
        response = requests.get(whisperAudioUrl.url, stream=True)
        if response.status_code == 200:
            with open("audio.mp3", "wb") as audio_file:
                shutil.copyfileobj(response.raw, audio_file)
            del response

            # Load the whisper model and transcribe the audio
            model = whisper.load_model("small")
            result = model.transcribe("audio.mp3")

            # Return the transcribed text
            item = {"detail": result["text"]}
            return JSONResponse(content=item, status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Failed to download audio file from the provided URL")
    except Exception as e:
        item = {"status": "failed", "message": str(e)}
        return JSONResponse(content=item, status_code=500)

@app.post("/transcribe-large/")
async def transcribe_audio_from_url(whisperAudioUrl: WhisperAudioURL):
    try:
        # Download the audio file from the provided URL
        response = requests.get(whisperAudioUrl.url, stream=True)
        if response.status_code == 200:
            with open("audio.mp3", "wb") as audio_file:
                shutil.copyfileobj(response.raw, audio_file)
            del response

            # Load the whisper model and transcribe the audio
            model = whisper.load_model("large")
            result = model.transcribe("audio.mp3")

            # Return the transcribed text
            item = {"detail": result["text"]}
            return JSONResponse(content=item, status_code=200)
        else:
            raise HTTPException(status_code=500, detail="Failed to download audio file from the provided URL")
    except Exception as e:
        item = {"status": "failed", "message": str(e)}
        return JSONResponse(content=item, status_code=500)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app with Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
