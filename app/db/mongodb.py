from pymongo import MongoClient
from app.db.config import settings

client = MongoClient(settings.MONGODB_URL)
if settings.MONGODB_DB_NAME is None:
    raise ValueError("MONGODB_DB_NAME must not be None")
db = client[settings.MONGODB_DB_NAME]

def get_database():
    return db
