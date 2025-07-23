"""Pyrogram plugin package for Rose bot."""

import importlib
import logging
import pkgutil
from typing import Any

LOGGER = logging.getLogger(__name__)
LOGGER.info("📦 Plugins package loaded")


def register_all(app: Any) -> None:
    """Import all plugin modules and register their handlers."""
    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name.startswith("_"):
            continue
        module = importlib.import_module(f"{__name__}.{module_info.name}")
        if hasattr(module, "register"):
            module.register(app)
            LOGGER.info("✅ Loaded plugin %s", module_info.name)
        else:
            LOGGER.warning("⚠️ Plugin %s has no register()", module_info.name)
