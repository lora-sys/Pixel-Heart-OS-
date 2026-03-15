"""
RelationshipRepository - Data access layer for Relationship model.
Each method acquires its own session from the global pool.
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from database import Relationship, get_session


class RelationshipRepository:
    """Repository for Relationship model operations."""

    async def create(self, relationship_data: Dict[str, Any]) -> Relationship:
        """Create a new relationship."""
        async with get_session() as session:
            relationship = Relationship(**relationship_data)
            session.add(relationship)
            await session.flush()
            await session.refresh(relationship)
            return relationship

    async def get_by_pair(
        self,
        character_id: str,
        target_character_id: str
    ) -> Optional[Relationship]:
        """Get relationship between two characters."""
        async with get_session() as session:
            stmt = select(Relationship).where(
                and_(
                    Relationship.character_id == character_id,
                    Relationship.target_character_id == target_character_id
                )
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_or_create(
        self,
        character_id: str,
        target_character_id: str,
        relationship_type: str,
        **defaults
    ) -> Relationship:
        """Get existing relationship or create new one."""
        async with get_session() as session:
            stmt = select(Relationship).where(
                and_(
                    Relationship.character_id == character_id,
                    Relationship.target_character_id == target_character_id
                )
            )
            result = await session.execute(stmt)
            relationship = result.scalar_one_or_none()

            if relationship is None:
                relationship_data = {
                    "character_id": character_id,
                    "target_character_id": target_character_id,
                    "relationship_type": relationship_type,
                    **defaults
                }
                relationship = Relationship(**relationship_data)
                session.add(relationship)
                await session.flush()
                await session.refresh(relationship)
            elif defaults:
                for key, value in defaults.items():
                    if hasattr(relationship, key):
                        setattr(relationship, key, value)
                await session.commit()
                await session.refresh(relationship)

            return relationship

    async def update_scores(
        self,
        character_id: str,
        target_character_id: str,
        trust_score: Optional[float] = None,
        emotional_intimacy: Optional[float] = None,
        conflict_level: Optional[float] = None,
        append_history: Optional[str] = None
    ) -> Optional[Relationship]:
        """Update relationship scores."""
        async with get_session() as session:
            stmt = select(Relationship).where(
                and_(
                    Relationship.character_id == character_id,
                    Relationship.target_character_id == target_character_id
                )
            )
            result = await session.execute(stmt)
            relationship = result.scalar_one_or_none()

            if relationship:
                if trust_score is not None:
                    relationship.trust_score = trust_score
                if emotional_intimacy is not None:
                    relationship.emotional_intimacy = emotional_intimacy
                if conflict_level is not None:
                    relationship.conflict_level = conflict_level
                if append_history is not None:
                    relationship.history.append(append_history)

                await session.commit()
                await session.refresh(relationship)

            return relationship

    async def list_for_character(
        self,
        character_id: str,
        relationship_type: Optional[str] = None
    ) -> List[Relationship]:
        """List all relationships for a character."""
        async with get_session() as session:
            stmt = select(Relationship).where(
                Relationship.character_id == character_id
            )
            if relationship_type:
                stmt = stmt.where(Relationship.relationship_type == relationship_type)
            result = await session.execute(stmt)
            return list(result.scalars().all())
