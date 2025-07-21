"""Utilities for automatically registering handlers."""

import asyncio
import importlib
import logging
import inspect
from pathlib import Path

from pyrogram import Client

LOGGER = logging.getLogger(__name__)

# Collect all Python files in handlers/, excluding private files and __init__.py
ALL_MODULES = [
    p.stem
    for p in Path(__file__).parent.glob("*.py")
    if not p.stem.startswith("_") and p.stem != "__init__"
]

async def register_all(app: Client) -> None:
    """Dynamically import all handler modules and call their register() functions."""

    LOGGER.info("📦 Registering all handlers...")

    for module_name in sorted(ALL_MODULES):
        module_path = f"handlers.{module_name}"

        try:
            module = importlib.import_module(module_path)
            LOGGER.debug("📦 Imported: %s", module_path)
        except Exception as import_err:
            LOGGER.exception("❌ Failed to import module '%s': %s", module_name, import_err)
            continue

        register_fn = getattr(module, "register", None)
        if not register_fn:
            LOGGER.warning("⚠️ No register() function found in %s", module_name)
            continue

        try:
            if inspect.iscoroutinefunction(register_fn):
                await register_fn(app)
            else:
                register_fn(app)
            LOGGER.info("✅ Handlers registered from: %s", module_name)
        except Exception as reg_err:
            LOGGER.exception("❌ Error calling register() in '%s': %s", module_name, reg_err)
