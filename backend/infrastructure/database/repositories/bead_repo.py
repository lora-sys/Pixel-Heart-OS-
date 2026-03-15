"""
BeadRepository - Data access layer for Bead model.
Each method acquires its own session from the global pool and closes it.
"""
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database import Bead, get_session


class BeadRepository:
    """Repository for Bead model operations."""

    async def create(self, bead_data: Dict[str, Any]) -> Bead:
        """Create a new bead in database."""
        async with get_session() as session:
            bead = Bead(**bead_data)
            session.add(bead)
            await session.flush()
            await session.refresh(bead)
            return bead

    async def get_by_id(self, bead_id: str) -> Optional[Bead]:
        """Get bead by ID."""
        async with get_session() as session:
            stmt = select(Bead).where(Bead.id == bead_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def get_timeline(
        self,
        branch_name: str,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Bead]:
        """Get timeline for a branch, ordered by timestamp."""
        async with get_session() as session:
            stmt = (
                select(Bead)
                .where(Bead.branch_name == branch_name)
                .order_by(Bead.timestamp.asc())
            )
            if limit is not None:
                stmt = stmt.limit(limit).offset(offset)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def get_head(self, branch_name: str) -> Optional[Bead]:
        """Get HEAD (latest) bead for a branch."""
        async with get_session() as session:
            stmt = (
                select(Bead)
                .where(Bead.branch_name == branch_name)
                .order_by(Bead.timestamp.desc())
                .limit(1)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def list_branches(self) -> Dict[str, Dict[str, Any]]:
        """List all branches and their HEAD beads."""
        async with get_session() as session:
            stmt = (
                select(
                    Bead.branch_name,
                    func.max(Bead.timestamp).label("max_ts")
                )
                .group_by(Bead.branch_name)
            )
            result = await session.execute(stmt)
            branch_data = result.all()

            branches = {}
            for branch_name, max_ts in branch_data:
                bead_stmt = select(Bead).where(
                    Bead.branch_name == branch_name,
                    Bead.timestamp == max_ts
                )
                bead_result = await session.execute(bead_stmt)
                head_bead = bead_result.scalar_one_or_none()
                if head_bead:
                    branches[branch_name] = {
                        "head_id": head_bead.id,
                        "head_timestamp": head_bead.timestamp.isoformat(),
                        "head_action": head_bead.action.value if hasattr(head_bead.action, 'value') else head_bead.action
                    }
            return branches

    async def get_children(self, parent_id: str) -> List[Bead]:
        """Get all direct children of a bead."""
        async with get_session() as session:
            stmt = select(Bead).where(Bead.parent_id == parent_id)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def delete(self, bead_id: str) -> bool:
        """Delete a bead."""
        async with get_session() as session:
            stmt = select(Bead).where(Bead.id == bead_id)
            result = await session.execute(stmt)
            bead = result.scalar_one_or_none()
            if bead:
                await session.delete(bead)
                await session.commit()
                return True
            return False
