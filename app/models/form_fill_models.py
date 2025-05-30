from pydantic import BaseModel

# Example POST endpoint to receive form data from UI
class FormData(BaseModel):
    title: str
    details: str
