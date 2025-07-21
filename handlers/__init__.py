"""Utilities for automatically registering handlers."""

import importlib
import logging
import inspect
from pathlib import Path

from pyrogram import Client

LOGGER = logging.getLogger(__name__)

# Collect all Python files in handlers/, excluding private files and __init__.py
ALL_MODULES = [
    file.stem
    for file in Path(__file__).parent.glob("*.py")
    if not file.stem.startswith("_") and file.stem != "__init__"
]

async def register_all(app: Client) -> None:
    """Dynamically import all modules and register their handlers."""
    for module_name in sorted(ALL_MODULES):
        module_path = f"handlers.{module_name}"
        try:
            module = importlib.import_module(module_path)
            LOGGER.debug("📦 Imported module: %s", module_path)
        except Exception as import_err:
            LOGGER.exception("❌ Failed to import module '%s': %s", module_name, import_err)
            continue

        try:
            # Call register(app) if it exists
            if hasattr(module, "register"):
                register_fn = getattr(module, "register")
                if inspect.iscoroutinefunction(register_fn):
                    await register_fn(app)
                else:
                    register_fn(app)

            # Register any manually-attached handlers (if using decorators)
            for attr in module.__dict__.values():
                if callable(attr) and hasattr(attr, "handlers"):
                    for handler, group in getattr(attr, "handlers"):
                        app.add_handler(handler, group=group)

            LOGGER.info("✅ Loaded handlers from: %s", module_name)

        except Exception as handler_err:
            LOGGER.exception("❌ Error initializing handlers in '%s': %s", module_name, handler_err)
