"""
Application lifecycle management.
Handles startup, shutdown, and resource cleanup.
"""

from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .container import Container
from config import Settings
import logging

logger = logging.getLogger(__name__)


def create_app(settings: Settings) -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(title="Pixel Heart OS API", version="0.1.0", debug=settings.debug)

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    from api.v1.router import api_router

    app.include_router(api_router, prefix="/api/v1")

    return app


class AppLifecycle:
    """Manages application lifecycle events."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.container: Optional[Container] = None

    def create_app(self) -> FastAPI:
        """Create and configure FastAPI application."""
        app = FastAPI(
            title="Pixel Heart OS API",
            version="0.1.0",
            debug=self.settings.debug,
            lifespan=lifespan
        )

        # Configure CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=self.settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Include API routers
        from api.v1.router import api_router
        app.include_router(api_router, prefix="/api/v1")

        # Store reference to lifecycle in app state
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
