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
