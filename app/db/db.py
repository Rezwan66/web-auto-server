# app/utils/db.py

import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("MONGODB_DB_NAME", "web_auto_metrics")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
