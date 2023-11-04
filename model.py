from pydantic import BaseModel

# Create a Pydantic model to define the request body
class WhisperAudioURL(BaseModel):
    url: str
