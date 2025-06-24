from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Explicit dotenv import
from dotenv import load_dotenv
load_dotenv()

# Imported Routes
from app.routes import form_fill_routes, llm_request_routes, automation_routes, test_db_routes, metrics_routes

app = FastAPI() # Starts the App

# Allow CORS (for frontend-backend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:5173"],  # For development only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import all route APIs
app.include_router(form_fill_routes.router, prefix="/formfill", tags=["FORM FILL"])
app.include_router(llm_request_routes.router, prefix="/llm", tags=["LLM"])
app.include_router(automation_routes.router, prefix="/automation", tags=["Automation"])
app.include_router(test_db_routes.router, prefix="/test", tags=["Test DB Connection"])
app.include_router(metrics_routes.router, prefix="/metrics", tags=["MongoDB"])

# Mock database (replace with real DB later)
fake_db = []

# Global home endpoint
@app.get("/")
async def root():
    return {"message": "Backend is running on port 8000"}
