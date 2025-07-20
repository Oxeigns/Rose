import logging
from functools import wraps
from pyrogram.types import Message

logger = logging.getLogger(__name__)

def catch_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception("Unhandled exception in handler: %s", e)
            if args and isinstance(args[-1], Message):
                try:
                    await args[-1].reply_text("⚠️ An unexpected error occurred.")
                except Exception:
                    pass
    return wrapper
