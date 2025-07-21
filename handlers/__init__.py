"""Utilities for automatically registering handlers."""

import importlib
import logging
import inspect
from pathlib import Path

from pyrogram import Client

LOGGER = logging.getLogger(__name__)

# Collect all Python modules in handlers/ (excluding private & __init__)
ALL_MODULES = [
    file.stem
    for file in Path(__file__).parent.glob("*.py")
    if not file.stem.startswith("_") and file.stem != "__init__"
]

async def register_all(app: Client) -> None:
    """Dynamically import all modules in 'handlers' and register their handlers."""

    for module_name in sorted(ALL_MODULES):
        module_path = f"handlers.{module_name}"

        try:
            module = importlib.import_module(module_path)
            LOGGER.debug("📦 Imported module: %s", module_path)
        except Exception as import_err:
            LOGGER.exception("❌ Failed to import '%s': %s", module_name, import_err)
            continue

        try:
            # Register function: register(app)
            if hasattr(module, "register"):
                register_fn = getattr(module, "register")

                if inspect.iscoroutinefunction(register_fn):
                    await register_fn(app)
                else:
                    register_fn(app)

            # Handle @decorator-attached handlers (Pyrogram 2.x)
            for attr in module.__dict__.values():
                if callable(attr) and hasattr(attr, "handlers"):
                    for item in getattr(attr, "handlers"):
                        try:
                            handler, value = item
                        except (TypeError, ValueError):
                            continue  # Invalid tuple format

                        if isinstance(value, int):
                            # (handler, group)
                            app.add_handler(handler, group=value)
                        else:
                            # (handler, filters)
                            rebuilt_handler = type(handler)(handler.callback, value)
                            app.add_handler(rebuilt_handler, group=0)

            LOGGER.info("✅ Loaded handlers from: %s", module_name)

        except Exception as handler_err:
            LOGGER.exception("❌ Error initializing '%s': %s", module_name, handler_err)
