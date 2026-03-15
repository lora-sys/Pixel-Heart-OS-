"""
CharacterRepository - Data access layer for Character model.
Each method acquires its own session from the global pool.
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import Character, Relationship, get_session


class CharacterRepository:
    """Repository for Character model operations."""

    async def create(self, character_data: Dict[str, Any]) -> Character:
        """Create a new character."""
        async with get_session() as session:
            character = Character(**character_data)
            session.add(character)
            await session.flush()
            await session.refresh(character)
            return character

    async def get_by_id(self, character_id: str) -> Optional[Character]:
        """Get character by ID."""
        async with get_session() as session:
            stmt = select(Character).where(Character.id == character_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_by_role(self, role: str) -> List[Character]:
        """Get characters by role."""
        async with get_session() as session:
            stmt = select(Character).where(Character.role == role)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def get_first_by_role(self, role: str) -> Optional[Character]:
        """Get first character with given role."""
        characters = await self.get_by_role(role)
        return characters[0] if characters else None

    async def list_all(self) -> List[Character]:
        """List all characters."""
        async with get_session() as session:
            stmt = select(Character)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def update(self, character_id: str, updates: Dict[str, Any]) -> Optional[Character]:
        """Update character fields."""
        async with get_session() as session:
            stmt = select(Character).where(Character.id == character_id)
            result = await session.execute(stmt)
            character = result.scalar_one_or_none()
            if character:
                for key, value in updates.items():
                    if hasattr(character, key):
                        setattr(character, key, value)
                await session.commit()
                await session.refresh(character)
            return character

    async def delete(self, character_id: str) -> bool:
        """Delete a character."""
        async with get_session() as session:
            stmt = select(Character).where(Character.id == character_id)
            result = await session.execute(stmt)
            character = result.scalar_one_or_none()
            if character:
                await session.delete(character)
                await session.commit()
                return True
            return False

    async def get_relationships(self, character_id: str) -> List[Relationship]:
        """Get all relationships for a character."""
        async with get_session() as session:
            stmt = select(Relationship).where(
                Relationship.character_id == character_id
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())
