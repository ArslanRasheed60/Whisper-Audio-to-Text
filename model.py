from pydantic import BaseModel
from typing import List

# Create a Pydantic model to define the request body
class WhisperAudioURL(BaseModel):
    url: str
    
class WhisperBashAudioURL(BaseModel):
    uid: str
    ids: List[str]
