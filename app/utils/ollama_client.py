from fastapi import HTTPException
import os
import httpx
from dotenv import load_dotenv
import time
from app.utils.extract_code import extract_code_block

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("DEFAULT_MODEL", "codeqwen")
# headers = {"Content-Type": "application/json"}
start = time.time()

async def generate_llm_response(prompt: str):
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            print('prompt utils:',prompt)
            response = await client.post(f"{OLLAMA_URL}/api/generate", headers={"Content-Type": "application/json"}, json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            })
            response.raise_for_status()  # Raises an error if HTTP response status is 4xx/5xx
            result = response.json()
            # content = response.json()
            # generated_text = content['response']['response']
            # print("Generated text:", generated_text)
            content = result.get("response") or result.get("message", {}).get("content", "")
            # print("Generated text: ", extract_code_block(content))
            print('utils: result:',extract_code_block(content))
            return extract_code_block(content)
    except httpx.TimeoutException:
            print("Timeout occurred! Try simplifying the prompt or using streaming.")        
    # except httpx.ReadTimeout as e:
    #     # Specific handling for timeout error
    #     raise HTTPException(status_code=504, detail="Request to the LLM service timed out.")
    except httpx.HTTPStatusError as e:
            # Properly get status_code and response text
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"HTTP error occurred: {e.response.text}")
    except httpx.RequestError as e:
        # General request errors (DNS issues, connection errors, etc.)
            raise HTTPException(status_code=503, detail=f"Error while requesting LLM service: {str(e)}")
    except Exception as e:
            # Catches any other unexpected error
            print("Error:", e)
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
    end = time.time()
    print(f"Duration: {end - start:.2f} seconds")
    # result = response.json()
    # return result.get("response") or result.get("message", {}).get("content", "")
