import ollama
from fastapi import HTTPException
import json
import os
from dotenv import load_dotenv
import time
from app.utils.extract_code import extract_code_block  # Ensure this is imported properly

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("DEFAULT_MODEL", "codeqwen")

def generate_with_ollama(prompt: str, metadata: dict) -> dict:
    """
    Calls ollama.chat to generate a Selenium code based on the prompt and metadata,
    and returns the generated code and the total duration.
    """
    try:
        # Build the metadata block, if metadata exists
        meta_block = f"\n\nPage metadata:\n{json.dumps(metadata, indent=2)}" if metadata else ""
        
        # Default URL if metadata URL is not provided
        url = metadata.get("url") if metadata else "http://localhost:5173/form"
        
        # Build the detailed prompt
        detailed_prompt = f"""
        Generate a complete, runnable Python Selenium script that does exactly this:
            1. Opens Chrome in **non-headless** mode.
            2. Navigates to {url}.
            3. Fills in the form fields as described below.
            4. Clicks the submit button.

        Task: {prompt}

        Instructions:
            - Use `webdriver.Chrome(options=options)` with `options.headless = False`.
            - Begin with all necessary imports.
            - Include `driver.get("{url}")`.
            - Locate elements by whatever selector is mentioned in the metadata first. 
            - Use `WebDriverWait` to wait for elements before `send_keys` or `click`.
            - Leave the browser window open at the end so the user can watch the result.
            - Only return the Python Selenium code (no extra commentary).
        
        {meta_block}
        """
        
        # Log the detailed prompt for debugging purposes
        print(f"Generated Prompt: {detailed_prompt}")

        # Use Ollama chat API to generate the code
        res = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{
                "role": "user", 
                "content": detailed_prompt
            }]
        )
        
        # Log Ollama response for debugging
        print(f"Ollama Response: {res}")

        # Extract the generated code
        full_text = res.get("message", {}).get("content", "")
        if not full_text:
            raise HTTPException(status_code=500, detail="Ollama returned no content.")
        
        # Ollama’s timing metric in nanoseconds – convert to ms
        total_ns = res.get("total_duration", 0)
        total_ms = total_ns // 1_000_000
        
        # Extract only the code from the response, if possible
        code_only = extract_code_block(full_text)

        return {
            "code": code_only if code_only is not None else full_text,
            "total_duration": total_ms,
            "model": res.get("model")
        }
    
    except Exception as e:
        # Catch any exceptions and log them
        print(f"Ollama Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")
