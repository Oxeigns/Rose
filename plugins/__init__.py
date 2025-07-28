"""Pyrogram plugin package for Rose bot with detailed error logging."""

import importlib
import logging
import pkgutil
import traceback
from typing import Any

LOGGER = logging.getLogger(__name__)
LOGGER.info("📦 Plugins package loaded")


def register_all(app: Any) -> int:
    """Import all plugin modules and register their handlers.

    Returns the number of successfully loaded modules.
    """
    loaded = 0
    for module_info in pkgutil.iter_modules(__path__):
        if module_info.name.startswith("_"):
            continue
        try:
            LOGGER.info("🔄 Importing plugin %s", module_info.name)
            module = importlib.import_module(f"{__name__}.{module_info.name}")
        except Exception:
            LOGGER.error(
                "❌ Failed to import plugin %s\n%s",
                module_info.name,
                traceback.format_exc()
            )
            continue

        if hasattr(module, "register"):
            try:
                module.register(app)
                loaded += 1
                LOGGER.info("✅ Loaded plugin %s", module_info.name)
            except Exception:
                LOGGER.error(
                    "❌ Error while registering handlers in %s\n%s",
                    module_info.name,
                    traceback.format_exc()
                )
        else:
            LOGGER.warning("⚠️ Plugin %s has no register()", module_info.name)

    LOGGER.info("📦 Plugin loading complete (%d modules)", loaded)
    return loaded
