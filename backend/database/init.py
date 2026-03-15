"""
Initialize database tables.
"""
import asyncio
from .engine import init_db

if __name__ == "__main__":
    asyncio.run(init_db())
