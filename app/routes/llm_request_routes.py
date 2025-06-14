from fastapi import APIRouter, HTTPException
import ollama
from app.utils.ollama_client import generate_llm_response, generate_with_ollama
from app.models.llm_request_model import LLMRequest

router = APIRouter()

# Using direct Ollama functions - less control
# @router.post('/generate')
# def generate(prompt: str):
#     response = ollama.chat(model='codeqwen',messages=[{'role':'user','content':prompt}])
#     return {'response':response['message']['content']}
@router.post('/generate')
def generate(request: LLMRequest):
    # request.prompt has the user’s raw prompt (from JSON body)
    generated_code = generate_with_ollama(request.prompt)
    print(generated_code)
    return {"response": generated_code}

# Using httpx / Requests - better control, flexibility
@router.post('/generate-llm')
async def generate_llm(request: LLMRequest):
    # response = await generate_llm_response(request.prompt)
    # print('routes:', response)
    # return {'response': response}
    try:
        # Generate Selenium Python code
        python_code = await generate_llm_response(request.prompt, language="python")

        # Generate JavaScript code for frontend automation
        js_code = await generate_llm_response(request.prompt, language="javascript")

        return {"python_code": python_code, "js_code": js_code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")
