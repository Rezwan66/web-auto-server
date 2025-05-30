from fastapi import APIRouter
import ollama
from app.utils.ollama_client import generate_llm_response
from app.models.llm_request_model import LLMRequest

router = APIRouter()

# Using direct Ollama functions - less control
@router.post('/generate')
def generate(prompt: str):
    response = ollama.chat(model='codeqwen',messages=[{'role':'user','content':prompt}])
    return {'response':response['message']['content']}

# Using httpx / Requests - better control, flexibility
@router.post('/generate-llm')
async def generate_llm(request: LLMRequest):
    response = await generate_llm_response(request.prompt)
    print('routes:', response)
    return {'response': response}
