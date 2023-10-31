from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import secrets

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


# Define an endpoint to create the Kubernetes Deployment
@app.post("/ai-transcribe-tiny")
async def create_deployment(data: Form()):
    try:
        item = {"status": "Success", "message": "Pod created successfully.", "pod_name": pod_name}
        return JSONResponse(content=item, status_code=201)
    except HTTPException as e:
        item = {"status": f"failed", "message": "An error occured while fetching the container status"}
        return JSONResponse(content=item, status_code=500)

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
