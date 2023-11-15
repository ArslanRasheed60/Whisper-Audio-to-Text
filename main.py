from fastapi import FastAPI, UploadFile, File
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
import shutil
from fastapi.middleware.cors import CORSMiddleware
import whisper
import shutil
import os
import requests
from collections import defaultdict
from threading import Thread
from queue import Queue
import time

from model import WhisperAudioURL, WhisperBashAudioURL
# firebase 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#user queues
user_queues = defaultdict(Queue)

app = FastAPI()

cred = credentials.Certificate('./whisper.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify the origins allowed here.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COLLECTION_USERS = "users"
SUB_COLLECTION_AUDIO = "AudioData"

@app.get("/testing")
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

@app.post("/transcribe-batch/")
async def transcribe_bashes(whisperBashIds: WhisperBashAudioURL):
    try:
        user_doc_id = whisperBashIds.uid
        sub_collec_id_list = whisperBashIds.ids
        print(user_doc_id,sub_collec_id_list)
        for sub_ids in sub_collec_id_list:
            print(sub_ids)
            doc_ref = db.collection(COLLECTION_USERS).document(user_doc_id).collection(SUB_COLLECTION_AUDIO).document(sub_ids)
            doc_dat = doc_ref.get()
            if doc_dat.exists:
                doc_data = doc_dat.to_dict()
                created_date_time = doc_data.get("createdDateTime")
                audio_url = doc_data.get("audio")
                model_type = doc_data.get("modelType")
                text = doc_data.get("text")
                print(f"Details:{model_type}, {text}, ")
                #Download the audio file from the provided URL
                response = requests.get(audio_url, stream=True)
                if response.status_code == 200:
                    with open("audio.mp3", "wb") as audio_file:
                        shutil.copyfileobj(response.raw, audio_file)
                    del response

                    # Load the whisper model and transcribe the audio
                    model = whisper.load_model(model_type)
                    result = model.transcribe("audio.mp3")
                    
                    doc_ref = db.collection(COLLECTION_USERS) \
                        .document(user_doc_id) 
                    doc_ref2 = doc_ref.collection(SUB_COLLECTION_AUDIO) \
                        .document(sub_ids) \
                        .update({"text": result["text"]})
                else:
                    doc_ref = db.collection(COLLECTION_USERS) \
                        .document(user_doc_id) 
                    doc_ref2 = doc_ref.collection(SUB_COLLECTION_AUDIO) \
                        .document(sub_ids) \
                        .update({"text": "Processing Failed"})
        
        return JSONResponse(content={"status": "Success"}, status_code=200)
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
