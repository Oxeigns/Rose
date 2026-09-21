"""HTTP health endpoint. Telegram updates arrive through Pyrogram MTProto."""

import os
from fastapi import FastAPI
import uvicorn

web_app = FastAPI()


@web_app.get("/")
@web_app.get("/healthz")
async def health():
    return {"status": "ok", "transport": "mtproto"}


def run() -> None:
    uvicorn.run(web_app, host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
