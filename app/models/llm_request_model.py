from pydantic import BaseModel

class LLMRequest(BaseModel):
    prompt: str # This is the user prompt sent to Ollama
#    model: str = ''
