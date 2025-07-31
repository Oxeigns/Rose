from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client.referbot

users_col = db.users
referrals_col = db.referrals
settings_col = db.settings
