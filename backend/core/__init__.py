"""
Core module for dependency injection and app lifecycle.
"""
from .container import Container
from .cache import Cache
from .lifecycle import AppLifecycle

__all__ = ["Container", "Cache", "AppLifecycle"]
