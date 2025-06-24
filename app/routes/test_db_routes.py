# app/routes/test_db_routes.py

from fastapi import APIRouter
from app.db.db import db

router = APIRouter()

@router.get("/db-health")
async def db_health():
    # list_collection_names will force a ping
    collections = await db.list_collection_names()
    return {"status": "ok", "collections": collections}
