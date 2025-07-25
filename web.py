"""FastAPI webhook app for handling Telegram updates."""

import logging
import os
from fastapi import FastAPI, Request
import uvicorn
from pyrogram import Client

LOGGER = logging.getLogger(__name__)

web_app = FastAPI()
_bot: Client | None = None


def setup(bot: Client) -> None:
    """Initialize webhook routes for the given bot."""
    global _bot
    _bot = bot

    @web_app.post("/")
    async def telegram_webhook(request: Request):
        data = await request.json()
        await _bot.process_webhook_update(data)
        return {"status": "ok"}


def run() -> None:
    """Run the FastAPI server."""
    port = int(os.getenv("PORT", "10000"))
    uvicorn.run(web_app, host="0.0.0.0", port=port)
