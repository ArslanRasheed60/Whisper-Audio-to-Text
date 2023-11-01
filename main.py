from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
from fastapi.middleware.cors import CORSMiddleware
import whisper

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
async def upload_audio_file(file: UploadFile = File(...)):
    try:
        with open("audio.mp3", "wb") as audio_file:
            shutil.copyfileobj(file.file, audio_file)

        # Load the whisper model and transcribe the audio
        model = whisper.load_model("tiny")
        print("reached tiny")
        result = model.transcribe("audio.mp3")

        # Return the transcribed text
        item = {"text": result["text"]}
        return JSONResponse(content=item, status_code=200)
    except HTTPException as e:
        item = {"status": f"failed", "message": "An error occured"}
        return JSONResponse(content=item, status_code=500)

@app.post("/transcribe-small/")
async def upload_audio_file(file: UploadFile = File(...)):
    try:
        with open("audio.mp3", "wb") as audio_file:
            shutil.copyfileobj(file.file, audio_file)

        # Load the whisper model and transcribe the audio
        model = whisper.load_model("small")
        print("reached small")
        result = model.transcribe("audio.mp3")

        # Return the transcribed text
        item = {"text": result["text"]}
        return JSONResponse(content=item, status_code=200)
    except HTTPException as e:
        item = {"status": f"failed", "message": "An error occured"}
        return JSONResponse(content=item, status_code=500)

@app.post("/transcribe-large/")
async def upload_audio_file(file: UploadFile = File(...)):
    try:
        with open("audio.mp3", "wb") as audio_file:
            shutil.copyfileobj(file.file, audio_file)

        # Load the whisper model and transcribe the audio
        model = whisper.load_model("large")
        print("reached large")
        result = model.transcribe("audio.mp3")

        # Return the transcribed text
        item = {"text": result["text"]}
        return JSONResponse(content=item, status_code=200)
    except HTTPException as e:
        item = {"status": f"failed", "message": "An error occured"}
        return JSONResponse(content=item, status_code=500)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app with Uvicorn
    uvicorn.run(app, host="143.244.137.207", port=8000)
    # uvicorn.run(app, host="127.0.0.1", port=8000)
