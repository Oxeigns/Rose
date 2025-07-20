"""Utilities for automatically registering handlers."""

import importlib
import logging
import inspect
from pathlib import Path

from pyrogram import Client

LOGGER = logging.getLogger(__name__)

# Collect all Python modules inside handlers/ excluding private files
ALL_MODULES = [
    file.stem
    for file in Path(__file__).parent.glob("*.py")
    if not file.stem.startswith("_")
]

async def register_all(app: Client) -> None:
    """Dynamically import all modules and register handlers if present."""
    for module_name in ALL_MODULES:
        try:
            module = importlib.import_module(f"handlers.{module_name}")
        except Exception as e:
            LOGGER.exception("❌ Failed to import module %s", module_name)
            continue

        try:
            # Register handler via register(app)
            if hasattr(module, "register"):
                reg = getattr(module, "register")
                if inspect.iscoroutinefunction(reg):
                    await reg(app)
                else:
                    reg(app)

            # Register decorator-based handlers manually
            for attr in module.__dict__.values():
                if callable(attr) and hasattr(attr, "handlers"):
                    for handler, group in getattr(attr, "handlers"):
                        app.add_handler(handler, group)

            LOGGER.info("✅ Loaded handler: %s", module_name)
        except Exception as err:
            LOGGER.exception("❌ Error loading handlers from %s: %s", module_name, err)
