import logging
import sys
from contextlib import suppress
from functools import wraps
from pyrogram.types import Message

logger = logging.getLogger(__name__)

def catch_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Log the exception without triggering recursion issues
            try:
                logger.exception(
                    "Unhandled exception in handler %s: %s",
                    func.__name__,
                    e,
                )
            except Exception:
                # Fallback to stderr if logging fails for some reason
                print(f"Logging failed for {func.__name__}: {e}", file=sys.stderr)

            # Attempt to notify the user about the failure
            if args and isinstance(args[-1], Message):
                with suppress(Exception):
                    await args[-1].reply_text("⚠️ An unexpected error occurred.")

            # Re-raise so outer wrappers or the event loop can handle it
            raise

    return wrapper
