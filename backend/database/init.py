"""Database initialization module for Pixel Heart OS."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base

# Database URL will be loaded from environment variables in main application
# This is just for standalone initialization/testing
DATABASE_URL = "sqlite+aiosqlite:///./data/pixel_heart_os.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """Initialize the database by creating all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


if __name__ == "__main__":
    import asyncio

    async def main():
        await init_db()
        print("Database initialized successfully!")

    asyncio.run(main())
