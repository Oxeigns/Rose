"""FastAPI webhook app for handling Telegram updates."""

import logging
import os
from fastapi import FastAPI, Request
import uvicorn
from pyrogram import Client
from typing import Optional

LOGGER = logging.getLogger(__name__)

web_app = FastAPI()
_bot: Optional[Client] = None


def setup(bot: Client) -> None:
    """Initialize webhook routes for the given bot."""
    global _bot
    _bot = bot

    @web_app.post("/")
    async def telegram_webhook(request: Request):
        data = await request.json()
        if _bot is None:
            LOGGER.error("Webhook received data but bot is not initialized.")
            return {"status": "bot not initialized"}
        try:
            await _bot.process_webhook_update(data)
        except Exception as e:
            LOGGER.exception("Error while processing webhook update: %s", e)
            return {"status": "error"}
        return {"status": "ok"}


def run() -> None:
    """Run the FastAPI server."""
    port = int(os.getenv("PORT", "10000"))
    LOGGER.info("Starting FastAPI webhook on port %d", port)
    uvicorn.run(web_app, host="0.0.0.0", port=port)
