from fastapi import APIRouter, HTTPException
import ollama
from app.utils.ollama_client import generate_llm_response, generate_with_ollama
from app.models.llm_request_model import LLMRequest
from app.utils.crud.metrics_crud import create_metric
from app.models.metrics_model import ExperimentMetrics
import time

router = APIRouter()

def sampleGenFunc(prompt: str) -> dict:
    print(prompt)
    return {
            "code": "Sample generated code",
            "total_duration": 200
        }

# Using direct Ollama functions - less control
# @router.post('/generate')
# def generate(prompt: str):
#     response = ollama.chat(model='codeqwen',messages=[{'role':'user','content':prompt}])
#     return {'response':response['message']['content']}
@router.post('/generate')
async def generate(request: LLMRequest):
    # request.prompt has the user’s raw prompt (from JSON body)
    start = time.perf_counter() # start api timer
    result = generate_with_ollama(request.prompt)
    # result = sampleGenFunc(request.prompt)
    api_time_ms = int((time.perf_counter() - start) * 1000)
    print(result, api_time_ms)
    # Build the metric to save to DB:
    metric = ExperimentMetrics(
        use_case="Form Filling",
        context_level="A",
        iteration=5,
        prompt=request.prompt,
        generation_duration_ms=result["total_duration"],
        api_time_ms=api_time_ms,
        generated_code=result["code"],  # Save the generated code
        model=result["model"] # LLM Model Used
    )
    # Log to MongoDB (await the insert)
    insert_response = await create_metric(metric)

    return {
        "response": result["code"],
        "generation_duration_ms": result["total_duration"],
        "api_time_ms": api_time_ms,
        "metric_id": str(insert_response.inserted_id)
    }

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
