import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.environ.get("MONGO_URL")
_client = AsyncIOMotorClient(MONGO_URL) if MONGO_URL else None

def get_db(name: str = "rose"):
    if not _client:
        raise RuntimeError("MONGO_URL not configured")
    return _client[name]
