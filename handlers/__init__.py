"""Utilities for automatically registering handlers."""

import asyncio
import importlib
import logging
import inspect
from pathlib import Path

from pyrogram import Client

LOGGER = logging.getLogger(__name__)

# Collect all Python modules in handlers/ (excluding private & __init__)
ALL_MODULES = [
    p.stem
    for p in Path(__file__).parent.glob("*.py")
    if not p.stem.startswith("_") and p.stem != "__init__"
]

async def register_all(app: Client) -> None:
    """Dynamically import all modules in 'handlers' and register their handlers."""

    for module_name in sorted(ALL_MODULES):
        module_path = f"handlers.{module_name}"
        try:
            module = importlib.import_module(module_path)
            LOGGER.debug("📦 Imported module: %s", module_path)
        except Exception:
            LOGGER.exception("Failed to import %s", module_path)
            continue

        register_fn = getattr(module, "register", None)
        if not register_fn:
            LOGGER.debug("No register() in %s", module_name)
            continue

        try:
            if inspect.iscoroutinefunction(register_fn):
                await register_fn(app)
            else:
                register_fn(app)
            LOGGER.info("✅ Handlers loaded from %s", module_name)
        except Exception:
            LOGGER.exception("Error running register() in %s", module_name)
