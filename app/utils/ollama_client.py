import ollama
from fastapi import HTTPException
import os
import httpx
from dotenv import load_dotenv
import time
from app.utils.extract_code import extract_code_block
import json

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("DEFAULT_MODEL", "codeqwen")
# headers = {"Content-Type": "application/json"}
start = time.time()

async def generate_llm_response(prompt: str, language: str):
     # Adjust the prompt depending on whether the user wants Python or JavaScript
    if language == "python":
        prompt = f"Generate a Selenium script in Python that automates the following task:\n{prompt}"
    elif language == "javascript":
        prompt = f"Generate JavaScript code that automates the following task on the frontend:\n{prompt}"
    
    try:
        async with httpx.AsyncClient() as client:
        # Send the prompt to Ollama (assuming you're using the local model)
            response = await client.post(f"{OLLAMA_URL}/api/generate", json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}, timeout=30)
            # Print raw response for debugging
            print(f"Raw Ollama response: {response.status_code}, {response.text}")
            response.raise_for_status()
            # Safely parse JSON and extract 'response' field
            json_data = response.json()
            if "response" not in json_data:
                raise HTTPException(status_code=500, detail=f"Ollama response missing 'response': {json_data}")
            return json_data["response"]
    except httpx.HTTPStatusError as e:
        # Specific error handling for HTTP errors
        print(f"HTTP error from Ollama: {e.response.status_code}, {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error from Ollama: {e.response.text}")
    except httpx.RequestError as e:
        # Request error (e.g., connection issues)
        print(f"Request error from Ollama: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        # Any other errors
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

def generate_with_ollama(prompt: str, metadata: dict) -> dict:
    """
    Calls ollama.chat with a detailed prompt (including metadata if given),
    extracts the first code block, and returns { code, total_duration, model }.
    """
    try:
        # Build the detailed prompt
        meta_block = f"\n\nPage metadata:\n{json.dumps(metadata, indent=2)}" if metadata else ""
        detailed_prompt = f"""
            Task: Produce a JSON array called "actions" for Playwright to automate this form.

            Prompt: {prompt}

            {meta_block}

            Each action must be:
            - {{ "type": "fill", "selector": "<selector>", "value": "<text>" }}
            - {{ "type": "click", "selector": "<selector>" }}
            - Only generate selectors which are present in the metadata
            
            Only output valid JSON like:
            {{ "actions": [ ... ] }}

        """
        # Use ollama.chat to generate a chat response
        res = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{
                "role": "user", 
                "content": detailed_prompt
            }]
        )
        payload = json.loads(res["message"]["content"])
        return payload["actions"]
        # Extract the generated text
        # print("ollama response -->",{res.get('model'),res.get('total_duration'), api_time_ms})
        # Ollama’s timing metric in nanoseconds – convert to ms
        total_ns = res.get("total_duration", 0)
        total_ms = total_ns // 1_000_000
        # full_text = res.get("message", {}).get("content", "")
        # if not full_text:
        #     raise HTTPException(status_code=500, detail="Ollama returned no content.")
        # Try to extract the code block:
        # code_only = extract_code_block(full_text)
        # return {
        #     # "code": code_only if code_only is not None else full_text,
        #     payload: payload["actions"],
        #     "total_duration": total_ms,
        #     "model": OLLAMA_MODEL
        # }
    
    except Exception as e:
        # Convert any exception into a proper HTTPException
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")
