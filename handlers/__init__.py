"""Utilities for automatically registering handlers."""

import importlib
import logging
from pathlib import Path

from pyrogram import Client

LOGGER = logging.getLogger(__name__)

# Collect all Python modules inside handlers/ excluding private files
ALL_MODULES = [
    file.stem
    for file in Path(__file__).parent.glob("*.py")
    if not file.stem.startswith("_")
]

def register_all(app: Client) -> None:
    """Dynamically import all modules and register handlers if present."""
    for module_name in ALL_MODULES:
        try:
            module = importlib.import_module(f"handlers.{module_name}")
        except Exception as e:
            LOGGER.exception("❌ Failed to import module %s", module_name)
            continue

        try:
            if hasattr(module, "register"):
                module.register(app)

            # If using Pyrogram @Client.on_* decorators
            for attr in module.__dict__.values():
                if callable(attr) and hasattr(attr, "handlers"):
                    for handler, group in getattr(attr, "handlers"):
                        app.add_handler(handler, group)

            LOGGER.info("✅ Loaded handler: %s", module_name)
        except Exception:
            LOGGER.exception("❌ Error loading handlers from %s", module_name)
