"""
Application lifecycle management.
Handles startup, shutdown, and resource cleanup.
"""
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .container import Container
from config import Settings


class AppLifecycle:
    """Manages application lifecycle events."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.container: Optional[Container] = None

    def create_app(self) -> FastAPI:
        """Create and configure FastAPI application."""
        from main import create_app

        # Store reference to lifecycle in app state
        app = create_app(self.settings)
        app.state.lifecycle = self

        return app

    async def startup(self) -> None:
        """Handle application startup."""
        # Initialize container
        from database import init_db
        from core.container import init_container
        self.container = init_container(self.settings)

        # Initialize database (create tables)
        await init_db()

        # ChromaDB client is lazy-initialized when first accessed

    async def shutdown(self) -> None:
        """Handle application shutdown."""
        # Close database connections
        from database import close_db
        await close_db()

        # Clear cache
        if self.container:
            self.container.get_cache().clear()

        # ChromaDB client doesn't need explicit close (handled by client)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.
    Handles startup and shutdown events.
    """
    lifecycle: AppLifecycle = app.state.lifecycle
    await lifecycle.startup()
    yield
    await lifecycle.shutdown()
