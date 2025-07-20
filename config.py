import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")

OWNER_ID = (
    int(os.environ.get("OWNER_ID", "0"))
    if os.environ.get("OWNER_ID")
    else None
)
LOG_GROUP_ID = (
    int(os.environ.get("LOG_GROUP_ID", "-1002867268050"))
    if os.environ.get("LOG_GROUP_ID")
    else None
)
