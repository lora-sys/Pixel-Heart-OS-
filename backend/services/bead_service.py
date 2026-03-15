"""
BeadService - Business logic for beads operations.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from beads.engine import BeadEngine
from infrastructure.database.repositories.bead_repo import BeadRepository
from core.cache import Cache
from database import ActionType, EmotionTag


class BeadService:
    """
    Service layer for bead operations.
    Combines BeadEngine (DAG logic) with repository (persistence) and cache.
    """

    def __init__(
        self,
        bead_engine: BeadEngine,
        bead_repo: BeadRepository,
        cache: Cache
    ):
        self.engine = bead_engine
        self.repository = bead_repo
        self.cache = cache

    async def create_bead(
        self,
        action: str,
        content: Dict[str, Any],
        parent_id: Optional[str] = None,
        branch_name: str = "main",
        emotion_tag: Optional[str] = None,
        signature: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new bead and persist it.

        Args:
            action: Action type (from ActionType enum)
            content: JSON-serializable content dictionary
            parent_id: Parent bead ID (optional)
            branch_name: Branch name (default "main")
            emotion_tag: Optional emotion tag
            signature: Optional signature for verification

        Returns:
            Created bead data dictionary
        """
        session = await self._get_session()
        try:
            # Delegate to engine (handles DAG validation, ID generation)
            bead = await self.engine.create_bead(
                action=action,
                content=content,
                parent_id=parent_id,
                branch_name=branch_name,
                emotion_tag=emotion_tag,
                signature=signature,
                session=session
            )

            # Since we passed our session, engine won't commit. Commit here.
            await session.commit()

            # Invalidate relevant cache entries
            await self._invalidate_timeline_cache(branch_name)
            await self._invalidate_head_cache(branch_name)

            return self._bead_to_dict(bead)
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def _get_session(self):
        """Get database session for service operations."""
        from database import get_session
        return await anext(get_session())

    async def get_timeline(
        self,
        branch_name: str = "main",
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get timeline for a branch with caching.

        First checks cache, then falls back to database.
        """
        cache_key = f"timeline:{branch_name}:{limit}:{offset}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        # Query from database via repository
        beads = await self.repository.get_timeline(
            branch_name=branch_name,
            limit=limit,
            offset=offset
        )

        result = [self._bead_to_dict(bead) for bead in beads]

        # Cache for 60 seconds
        self.cache.set(cache_key, result, ttl=60)

        return result

    async def get_bead(self, bead_id: str) -> Optional[Dict[str, Any]]:
        """Get a single bead by ID."""
        # Could cache individual beads if needed
        bead = await self.repository.get_by_id(bead_id)
        return self._bead_to_dict(bead) if bead else None

    async def get_head(self, branch_name: str = "main") -> Optional[Dict[str, Any]]:
        """Get HEAD bead for a branch."""
        cache_key = f"head:{branch_name}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        head = await self.repository.get_head(branch_name)
        result = self._bead_to_dict(head) if head else None

        self.cache.set(cache_key, result, ttl=30)
        return result

    async def list_branches(self) -> Dict[str, Dict[str, Any]]:
        """List all branches."""
        cache_key = "branches:all"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        branches = await self.repository.list_branches()
        self.cache.set(cache_key, branches, ttl=120)
        return branches

    async def create_branch(
        self,
        branch_name: str,
        from_bead_id: str
    ) -> Dict[str, Any]:
        """
        Create a new branch from a given bead.

        Args:
            branch_name: Name for new branch
            from_bead_id: Bead ID to branch from

        Returns:
            Branch info (name, head_bead_id)
        """
        session = await self._get_session()
        try:
            # Use engine to validate branch creation (no DB write)
            branch_name_result, head_bead = await self.engine.create_branch(
                branch_name=branch_name,
                from_bead_id=from_bead_id,
                session=session
            )

            await session.commit()

            # Invalidate caches
            await self._invalidate_timeline_cache(branch_name)
            await self._invalidate_timeline_cache("main")
            await self._invalidate_branches_cache()

            return {
                "branch_name": branch_name_result,
                "head_bead_id": head_bead.id,
                "message": f"Branch '{branch_name_result}' created from bead {from_bead_id[:8]}"
            }
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def diff_beads(
        self,
        bead_id1: str,
        bead_id2: str
    ) -> Dict[str, Any]:
        """
        Compute diff between two beads.

        Args:
            bead_id1: First bead ID (earlier/ancestor)
            bead_id2: Second bead ID (later/descendant)

        Returns:
            Diff data with bead IDs and changes list
        """
        session = await self._get_session()
        try:
            changes = await self.engine.diff_beads(bead_id1, bead_id2, session=session)

            # Determine which is earlier/later by timestamp (use repository)
            bead1 = await self.repository.get_by_id(bead_id1)
            bead2 = await self.repository.get_by_id(bead_id2)

            if not bead1 or not bead2:
                raise ValueError("One or both beads not found")

            earlier_id = bead_id1 if bead1.timestamp < bead2.timestamp else bead_id2
            later_id = bead_id2 if bead2.timestamp > bead1.timestamp else bead_id1

            return {
                "bead_id_earlier": earlier_id,
                "bead_id_later": later_id,
                "changes": changes
            }
        finally:
            await session.close()

    async def rebase_branch(
        self,
        branch_name: str,
        onto_bead_id: str
    ) -> List[Dict[str, Any]]:
        """
        Rebase branch onto new base.
        Creates new beads with different parent IDs.

        Returns:
            List of new rebased beads
        """
        session = await self._get_session()
        try:
            new_beads = await self.engine.rebase_branch(
                branch_name=branch_name,
                onto_bead_id=onto_bead_id,
                session=session
            )

            await session.commit()

            # Invalidate caches for affected branch
            await self._invalidate_timeline_cache(branch_name)
            await self._invalidate_head_cache(branch_name)
            await self._invalidate_branches_cache()

            return [self._bead_to_dict(bead) for bead in new_beads]
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def merge_branches(
        self,
        source_branch: str,
        target_branch: str,
        strategy: str = "auto"
    ) -> Dict[str, Any]:
        """
        Merge source branch into target branch.
        Creates a merge bead representing the merge point.
        """
        session = await self._get_session()
        try:
            merge_bead = await self.engine.merge_branches(
                source_branch=source_branch,
                target_branch=target_branch,
                strategy=strategy,
                session=session
            )

            await session.commit()

            # Invalidate caches
            await self._invalidate_timeline_cache(target_branch)
            await self._invalidate_head_cache(target_branch)
            await self._invalidate_branches_cache()

            return self._bead_to_dict(merge_bead)
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def _invalidate_timeline_cache(self, branch_name: str) -> None:
        """Invalidate all timeline cache entries for a branch."""
        # Simple approach: clear all keys starting with pattern
        # More precise: track exact keys used
        import re
        # For now, we can't iterate over private store in thread-safe way
        # So we just clear entire cache on structural changes
        # TODO: Implement pattern-based invalidation if needed
        pass

    async def _invalidate_head_cache(self, branch_name: str) -> None:
        """Invalidate HEAD cache for branch."""
        self.cache.delete(f"head:{branch_name}")

    async def _invalidate_branches_cache(self) -> None:
        """Invalidate branches list cache."""
        self.cache.delete("branches:all")

    def _bead_to_dict(self, bead: Any) -> Dict[str, Any]:
        """Convert Bead object to API response dictionary."""
        if bead is None:
            return None

        return {
            "id": bead.id,
            "parent_id": bead.parent_id,
            "branch_name": bead.branch_name,
            "timestamp": bead.timestamp.isoformat() if isinstance(bead.timestamp, datetime) else bead.timestamp,
            "action": bead.action.value if hasattr(bead.action, 'value') else bead.action,
            "emotion_tag": bead.emotion_tag.value if bead.emotion_tag and hasattr(bead.emotion_tag, 'value') else bead.emotion_tag,
            "content": bead.content,
            "signature": bead.signature
        }
