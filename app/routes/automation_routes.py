import subprocess, tempfile, os, sys
from fastapi import APIRouter, HTTPException
from app.utils.automation import fill_form

router = APIRouter()

@router.post("/fill-form")
async def fill_form_route(title: str, details: str):
    try:
        fill_form(title, details) # to run the form-filling script
        return {"status": "Success!", "message": "Form filled successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fill form: {str(e)}")


@router.post("/run-python-code")
async def run_python_code(request: dict):
    """
    Expects JSON body like { "code": "<Python code here>" }.
    Writes the code to a UTF-8 temp file, runs it with the current venv
    interpreter (sys.executable), captures stdout/stderr.
    """
    code = request.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="No code provided!")
    
    # Create a temporary file to hold the Python code
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp_filename = tmp.name
        tmp.write(code)
    
    try:
        # Run the temp file with Python
        # Write the code to a temporary file, or run via -c directly
        # For simplicity, we’ll run via '-c'
        result = subprocess.run(
            [sys.executable, tmp_filename],
            capture_output=True,
            text=True,
            timeout=60
        )
        # Delete the temp file
        os.remove(tmp_filename)

        if result.returncode != 0:
            # If the Python script crashed, send back stderr
            raise HTTPException(status_code=500, detail=f"Selenium error: {result.stderr}")
        
        print("backend result:>",result)
        return {"status": "success", "output": result.stdout}
    
    except subprocess.TimeoutExpired:
        # In case the script hangs
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)
        raise HTTPException(status_code=504, detail="Code execution timed out.")
    except HTTPException:
        # Re-raise our own HTTPException (so the message gets passed through)
        raise
    except Exception as e:
        # Any other unexpected error
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)
        raise HTTPException(status_code=500, detail=f"Error running code: {str(e)}")
