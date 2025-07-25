"""Pyrogram plugin package for Rose bot."""

import importlib
import logging
import pkgutil
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
            module = importlib.import_module(f"{__name__}.{module_info.name}")
        except Exception as e:  # pragma: no cover - import errors should abort
            LOGGER.exception("❌ Failed loading %s: %s", module_info.name, e)
            continue

        if hasattr(module, "register"):
            try:
                module.register(app)
                loaded += 1
                LOGGER.info("✅ Loaded plugin %s", module_info.name)
            except Exception as e:  # pragma: no cover - handler errors should show
                LOGGER.exception("❌ Error registering %s: %s", module_info.name, e)
        else:
            LOGGER.warning("⚠️ Plugin %s has no register()", module_info.name)

    LOGGER.info("📦 Plugin loading complete (%d modules)", loaded)
    return loaded
