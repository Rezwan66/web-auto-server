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
        url = metadata.get("url") if metadata else "http://localhost:5173/form"
        detailed_prompt = f"""
            Generate a complete, runnable Python Selenium script that does exactly this:
                1. Opens Chrome in **non-headless** mode.
                2. Navigates to {url}.
                3. Fills in the form fields as described below.
                4. Clicks the submit button.

            Task: {prompt}

            Instructions for the code:
                - Use `webdriver.Chrome(options=options)` with `options.headless = False`.
                - Begin with all necessary imports.
                - Include `driver.get("{url}")`.
                - Locate elements by whatever selector is mentioned in the metadata first. 
                - Use `WebDriverWait` to wait for elements before `send_keys` or `click`.
                - Leave the browser window open at the end so the user can watch the result.
                - Only return the Python Selenium code (no extra commentary).
        """
        small_test_prompt = "Write a Python code to find the first 100 prime numbers."
        print(f"Detailed Prompt: {detailed_prompt}")
        print(f"Metadata: {meta_block}")
        print(f"Metadata without json dumptruck: {metadata}")
        # Use ollama.chat to generate a chat response
        # res = ollama.chat(
        #     model=OLLAMA_MODEL,
        #     messages=[{
        #         "role": "user", 
        #         "content": detailed_prompt
        #     }]
        # )
        res = {
            "total_duration": 69,
            "message": {"content": 'test'}
        }
        # Log the raw response from Ollama for debugging
        print(f"Ollama Response: {res}")
        # payload = json.loads(res["message"]["content"])
        # return {"success": "success"}
        # Extract the generated text
        # print("ollama response -->",{res.get('model'),res.get('total_duration'), api_time_ms})
        # Ollama’s timing metric in nanoseconds – convert to ms
        total_ns = res.get("total_duration", 0)
        total_ms = total_ns // 1_000_000
        full_text = res.get("message", {}).get("content", "")
        if not full_text:
            raise HTTPException(status_code=500, detail="Ollama returned no content.")
        # Try to extract the code block:
        code_only = extract_code_block(full_text)
        return {
            "code": code_only if code_only is not None else full_text,
            # payload: payload["actions"],
            "total_duration": total_ms,
            "model": OLLAMA_MODEL
        }
    
    except Exception as e:
        # Convert any exception into a proper HTTPException
        print(f"Ollama Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")
