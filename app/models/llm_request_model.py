from pydantic import BaseModel
from typing import Optional, Any

class LLMRequest(BaseModel):
    prompt: str # This is the user prompt sent to Ollama
#    model: str = ''
    metadata: Optional[Any] = None  # will hold the JSON form schema
