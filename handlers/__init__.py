import importlib
from pathlib import Path

ALL_MODULES = []
for file in Path(__file__).parent.glob('*.py'):
    if file.stem.startswith('_'):
        continue
    ALL_MODULES.append(file.stem)


def register_all(app):
    for module_name in ALL_MODULES:
        module = importlib.import_module(f'handlers.{module_name}')
        if hasattr(module, 'register'):
            module.register(app)
        # Support modules that use the ``@Client.on_*`` decorators without
        # providing an explicit ``register`` function. Those decorators attach
        # handler information to the decorated callables via a ``handlers``
        # attribute which we can use to register them here.
        for attr in module.__dict__.values():
            if callable(attr) and hasattr(attr, "handlers"):
                for handler, group in getattr(attr, "handlers"):
                    app.add_handler(handler, group)
