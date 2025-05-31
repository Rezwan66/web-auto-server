from fastapi import APIRouter
from app.models.form_fill_models import FormData

router = APIRouter()

# Example GET endpoint for testing
@router.get("/get-form-data")
async def get_form_data():
    return {"data": "This is data from the backend GET endpoint. Alu kalu balu"}

@router.post("/submit-form")
async def submit_form(data: FormData):
    # For now, just echo the data back to frontend
    return {
        "status": "success",
        "received": {
            "title": data.title,
            "details": data.details
        }
    }
