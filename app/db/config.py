import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URL = os.getenv("MONGODB_URL")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

settings = Settings()
