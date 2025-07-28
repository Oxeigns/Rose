"""Pyrogram plugin package for Rose bot with detailed error logging."""

import importlib
import logging
import traceback
from pathlib import Path
from typing import Any

LOGGER = logging.getLogger(__name__)
LOGGER.info("📦 Plugins package loaded")


def register_all(app: Any) -> int:
    """Import all plugin modules and register their handlers.

    Returns the number of successfully loaded modules.
    """
    loaded = 0
    plugin_dir = Path(__file__).parent
    for file in sorted(plugin_dir.glob("*.py")):
        if file.name == "__init__.py":
            continue
        module_name = f"{__name__}.{file.stem}"
        try:
            LOGGER.info("🔄 Importing plugin %s", file.stem)
            module = importlib.import_module(module_name)
        except Exception:
            LOGGER.warning(
                "❌ Failed to import plugin %s\n%s",
                file.stem,
                traceback.format_exc()
            )
            continue

        if hasattr(module, "register"):
            try:
                module.register(app)
                loaded += 1
                LOGGER.info("✅ Loaded plugin %s", file.stem)
            except Exception:
                LOGGER.warning(
                    "❌ Error while registering handlers in %s\n%s",
                    file.stem,
                    traceback.format_exc()
                )
        else:
            LOGGER.warning("⚠️ Plugin %s has no register()", file.stem)

    LOGGER.info("📦 Plugin loading complete (%d modules)", loaded)
    return loaded
