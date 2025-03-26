# connection/__init__.py (optional)
from importlib import import_module
from pkgutil import walk_packages

# Import base Connection class first
from .base import Connection  # noqa: F401

# Auto-import all subclasses of Connection
for _, name, _ in walk_packages(__path__):
    import_module(f"{__name__}.{name}")
