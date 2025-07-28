import logging
import sys
from contextlib import suppress
from functools import wraps
from pyrogram.types import Message, CallbackQuery

logger = logging.getLogger(__name__)

def catch_errors(func):
    """
    Decorator for safely catching and logging exceptions in handlers.
    Ensures errors are logged and a user-friendly error message is sent.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Log the exception
            try:
                logger.exception(
                    "Unhandled exception in handler %s: %s",
                    func.__name__,
                    e,
                )
            except Exception:
                # Fallback to stderr if logging fails
                print(f"Logging failed for {func.__name__}: {e}", file=sys.stderr)

            # Try to notify the user gracefully
            target = None
            # Look for Message or CallbackQuery in args
            for arg in args:
                if isinstance(arg, Message):
                    target = arg
                    break
                if isinstance(arg, CallbackQuery):
                    target = arg
                    break

            if target:
                with suppress(Exception):
                    if isinstance(target, Message):
                        await target.reply_text("⚠️ An unexpected error occurred.")
                    elif isinstance(target, CallbackQuery):
                        await target.answer("⚠️ An unexpected error occurred.", show_alert=True)

            # Do not re-raise; swallow the exception after logging
            # to avoid Pyrogram stopping the handler chain.
            return None

    return wrapper
