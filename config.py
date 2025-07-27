"""Configuration module for environment variables."""

import os
from dotenv import load_dotenv

# Load variables from .env file (if present)
load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")

# Optional owner ID (can be None)
OWNER_ID_ENV = os.getenv("OWNER_ID")
OWNER_ID = int(OWNER_ID_ENV) if OWNER_ID_ENV else None

# Logging group (disabled if None)
LOG_GROUP_ID = None
