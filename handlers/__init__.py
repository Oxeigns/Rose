"""Utilities for automatically registering handlers."""

import importlib
import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)

ALL_MODULES = []
for file in Path(__file__).parent.glob('*.py'):
    if file.stem.startswith('_'):
        continue
    ALL_MODULES.append(file.stem)


def register_all(app):
    """Dynamically import handler modules and register them with ``app``."""

    for module_name in ALL_MODULES:
        try:
            module = importlib.import_module(f"handlers.{module_name}")
        except Exception:
            LOGGER.exception("Failed to import handler module %s", module_name)
            continue

        try:
            if hasattr(module, "register"):
                module.register(app)

            # Support modules that rely on ``@Client.on_*`` decorators
            for attr in module.__dict__.values():
                if callable(attr) and hasattr(attr, "handlers"):
                    for handler, group in getattr(attr, "handlers"):
                        app.add_handler(handler, group)
            LOGGER.info("Loaded handler: %s", module_name)
        except Exception:
            LOGGER.exception("Error loading handlers from %s", module_name)
