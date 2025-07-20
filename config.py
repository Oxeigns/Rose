import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "123456"))
API_HASH = os.environ.get("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN")

# Directly assign fixed values here
OWNER_ID = 1888832817  # Replace with your actual Telegram user ID
LOG_GROUP_ID = -1002867268050  # Replace with your actual group/channel ID
