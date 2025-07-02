from fastapi import APIRouter, HTTPException
import ollama
from starlette.concurrency import run_in_threadpool
from app.utils.ollama_client import generate_llm_response, generate_with_ollama
from app.models.llm_request_model import LLMRequest
from app.utils.crud.metrics_crud import create_metric
from app.models.metrics_model import ExperimentMetrics
from app.utils.validate_selectors import validate_actions_sync
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
    metadata = request.metadata or {}
    start = time.perf_counter() # start api timer
    # for attempt in range(3):
    try:
        result = generate_with_ollama(request.prompt, metadata)
             # Compute selector accuracy
                # Offload the sync Playwright call to a thread
            # selector_accuracy = await run_in_threadpool(
            #         validate_actions_sync, result, metadata.get("url", "")
            # )
        print(result)
           
    # result = sampleGenFunc(request.prompt)
    except Exception as e:
            # if attempt == 2:
        raise HTTPException(status_code=500, detail=f"Error generating code: {str(e)}")
            # time.sleep(1)  # brief back‑off
    finally:
        api_time_ms = int((time.perf_counter() - start) * 1000)
    
    # Build the metric to save to DB:
    # metric = ExperimentMetrics(
        # use_case="Form Filling",
        # context_level="A",
        # iteration=6,
        # prompt=request.prompt,
        # generation_duration_ms=result["total_duration"],
        # api_time_ms=api_time_ms,
        # generated_code=result["code"],  # Save the generated code
        # model=result["model"] # LLM Model Used
    # )
    # Log to MongoDB (await the insert)
    # insert_response = await create_metric(metric)

    return {
        # "response": result["code"],
        # "generation_duration_ms": result["total_duration"],
        "actions": result,
        # "selector_accuracy": selector_accuracy,
        "api_time_ms": api_time_ms,
        # "metric_id": str(insert_response.inserted_id)
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
