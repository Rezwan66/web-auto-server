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
