"""
Beads Engine: Git-like DAG narrative state management.
"""
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, and_, func
import hashlib
import json

from database import Bead, get_session, ActionType, EmotionTag


class BeadEngine:
    """
    Core engine for managing Beads DAG.
    Provides branching, merging, rebasing, and timeline traversal.
    """

    def __init__(self):
        # No session stored as instance variable! Each call must receive a session.
        pass

    async def _get_session(self, session: Optional[AsyncSession] = None) -> AsyncSession:
        """
        Get session to use. If provided, use it; else create new (for standalone use).
        Services should always provide a session.
        """
        if session is not None:
            return session
        # Fallback: create new session (not recommended for production)
        return await anext(get_session())

    async def _sha1_hash(self, parent_id: Optional[str], content: Dict[str, Any], action: str) -> str:
        """Calculate SHA-1 hash for bead ID."""
        hash_input = {
            "parent": parent_id or "",
            "content": content,
            "action": action,
            "timestamp": datetime.utcnow().isoformat()
        }
        hash_str = json.dumps(hash_input, sort_keys=True, separators=(',', ':'))
        return hashlib.sha1(hash_str.encode('utf-8')).hexdigest()

    async def create_bead(
        self,
        action: str,
        content: Dict[str, Any],
        parent_id: Optional[str] = None,
        branch_name: str = "main",
        emotion_tag: Optional[str] = None,
        signature: Optional[str] = None,
        session: Optional[AsyncSession] = None
    ) -> Bead:
        """
        Create a new Bead and attach it to the DAG.
        Validates DAG structure (no cycles).

        Args:
            session: Optional database session. Services should provide request-scoped session.
        """
        sess = await self._get_session(session)

        # Validate parent exists (if provided)
        if parent_id:
            stmt = select(Bead).where(Bead.id == parent_id)
            result = await sess.execute(stmt)
            parent = result.scalar_one_or_none()
            if not parent:
                raise ValueError(f"Parent bead {parent_id} not found")

            # Check that adding this child doesn't create a cycle
            if await self._would_create_cycle(parent_id, parent.branch_name, branch_name, session=sess):
                raise ValueError("Adding this bead would create a cycle in the DAG")

        # Calculate bead ID
        bead_id = await self._sha1_hash(parent_id, content, action)

        # Check for duplicate ID (extremely unlikely but safe)
        existing = await sess.execute(select(Bead).where(Bead.id == bead_id))
        if existing.scalar_one_or_none():
            # Collision - add timestamp suffix
            bead_id = bead_id[:38] + datetime.utcnow().strftime("%S")[-2:]

        # Create bead
        bead = Bead(
            id=bead_id,
            parent_id=parent_id,
            branch_name=branch_name,
            action=ActionType(action),
            emotion_tag=EmotionTag(emotion_tag) if emotion_tag else None,
            content=content,
            signature=signature
        )

        sess.add(bead)
        await sess.flush()
        await sess.refresh(bead)

        # Don't commit here - let caller's session commit at appropriate time
        # But original design had commit here. Need to decide.
        # For now, commit immediately (as before) but only if we own the session
        if session is None:
            # We created our own session, so we commit
            await sess.commit()
        # If session was provided, don't commit - caller will commit

        return bead

    async def _would_create_cycle(
        self,
        start_id: str,
        start_branch: str,
        target_branch: str,
        session: Optional[AsyncSession] = None
    ) -> bool:
        """Check if adding a bead would create a cycle."""
        sess = await self._get_session(session)

        # If target_branch == start_branch, cannot add child that is already an ancestor
        if target_branch == start_branch:
            current_id = start_id
            while current_id:
                stmt = select(Bead).where(Bead.id == current_id)
                result = await sess.execute(stmt)
                current = result.scalar_one_or_none()
                if not current:
                    break
                if current.branch_name == target_branch and current_id != start_id:
                    return True
                current_id = current.parent_id

        return False

    async def get_timeline(
        self,
        branch_name: str = "main",
        limit: Optional[int] = None,
        session: Optional[AsyncSession] = None
    ) -> List[Bead]:
        """
        Get timeline for a branch, ordered by timestamp ascending.

        Args:
            branch_name: Branch to query
            limit: Maximum number of beads
            session: Optional session
        """
        sess = await self._get_session(session)

        stmt = (
            select(Bead)
            .where(Bead.branch_name == branch_name)
            .order_by(Bead.timestamp.asc())
        )

        if limit:
            stmt = stmt.limit(limit)

        result = await sess.execute(stmt)
        return list(result.scalars().all())

    async def get_head(self, branch_name: str = "main", session: Optional[AsyncSession] = None) -> Optional[Bead]:
        """Get HEAD (latest) bead for a branch."""
        beads = await self.get_timeline(branch_name, session=session)
        return beads[-1] if beads else None

    async def get_branch_point(self, bead_id1: str, bead_id2: str, session: Optional[AsyncSession] = None) -> Optional[Bead]:
        """Find the common ancestor (merge base) of two beads."""
        sess = await self._get_session(session)

        # Get ancestors of bead1
        ancestors1 = set()
        current = bead_id1
        while current:
            ancestors1.add(current)
            stmt = select(Bead).where(Bead.id == current)
            result = await sess.execute(stmt)
            bead = result.scalar_one_or_none()
            if not bead:
                break
            current = bead.parent_id

        # Walk up from bead2
        current = bead_id2
        while current:
            if current in ancestors1:
                stmt = select(Bead).where(Bead.id == current)
                result = await sess.execute(stmt)
                return result.scalar_one_or_none()
            stmt = select(Bead).where(Bead.id == current)
            result = await sess.execute(stmt)
            bead = result.scalar_one_or_none()
            if not bead:
                break
            current = bead.parent_id

        return None

    async def create_branch(
        self,
        branch_name: str,
        from_bead_id: str,
        session: Optional[AsyncSession] = None
    ) -> Tuple[str, Bead]:
        """Create a new branch starting from a given bead."""
        sess = await self._get_session(session)

        stmt = select(Bead).where(Bead.id == from_bead_id)
        result = await sess.execute(stmt)
        from_bead = result.scalar_one_or_none()
        if not from_bead:
            raise ValueError(f"Source bead {from_bead_id} not found")

        existing_head = await self.get_head(branch_name, session=sess)
        if existing_head:
            raise ValueError(f"Branch '{branch_name}' already exists")

        return branch_name, from_bead

    async def merge_branches(
        self,
        source_branch: str,
        target_branch: str,
        strategy: str = "auto",
        session: Optional[AsyncSession] = None
    ) -> Bead:
        """Merge source branch into target branch."""
        sess = await self._get_session(session)

        source_head = await self.get_head(source_branch, session=sess)
        target_head = await self.get_head(target_branch, session=sess)

        if not source_head:
            raise ValueError(f"Source branch '{source_branch}' is empty")
        if not target_head:
            source_head.branch_name = target_branch
            await sess.commit()
            return source_head

        if await self._is_ancestor(source_head.id, target_head.id, session=sess):
            pass

        merge_content = {
            "merge_source": source_branch,
            "merge_target": target_branch,
            "source_head": source_head.id,
            "target_head": target_head.id,
            "strategy": strategy
        }

        merge_bead = await self.create_bead(
            action="merge",
            content=merge_content,
            parent_id=target_head.id,
            branch_name=target_branch,
            emotion_tag="neutral",
            session=sess
        )

        return merge_bead

    async def _is_ancestor(self, candidate_id: str, descendant_id: str, session: Optional[AsyncSession] = None) -> bool:
        """Check if candidate is an ancestor of descendant."""
        sess = await self._get_session(session)

        current = descendant_id
        while current:
            if current == candidate_id:
                return True
            stmt = select(Bead).where(Bead.id == current)
            result = await sess.execute(stmt)
            bead = result.scalar_one_or_none()
            if not bead:
                break
            current = bead.parent_id

        return False

    async def rebase_branch(
        self,
        branch_name: str,
        onto_bead_id: str,
        session: Optional[AsyncSession] = None
    ) -> List[Bead]:
        """Rebase branch onto new base."""
        sess = await self._get_session(session)

        branch_head = await self.get_head(branch_name, session=sess)
        if not branch_head:
            raise ValueError(f"Branch '{branch_name}' is empty")

        stmt = select(Bead).where(Bead.id == onto_bead_id)
        result = await sess.execute(stmt)
        onto_bead = result.scalar_one_or_none()
        if not onto_bead:
            raise ValueError(f"Base bead {onto_bead_id} not found")

        common_ancestor = await self.get_branch_point(branch_head.id, onto_bead_id, session=sess)
        if not common_ancestor:
            raise ValueError("No common ancestor found")

        commits = await self._collect_commits_after(common_ancestor.id, branch_head.id, session=sess)

        new_beads = []
        current_parent_id = onto_bead_id

        for commit in reversed(commits):
            new_bead = await self.create_bead(
                action=commit.action,
                content=commit.content,
                parent_id=current_parent_id,
                branch_name=branch_name,
                emotion_tag=commit.emotion_tag,
                signature=commit.signature,
                session=sess
            )
            new_beads.append(new_bead)
            current_parent_id = new_bead.id

        if session is None:
            await sess.commit()

        return new_beads

    async def _collect_commits_after(
        self,
        ancestor_id: str,
        descendant_id: str,
        session: Optional[AsyncSession] = None
    ) -> List[Bead]:
        """Collect commits from ancestor (exclusive) to descendant (inclusive)."""
        sess = await self._get_session(session)

        path = []
        current = descendant_id
        while current and current != ancestor_id:
            stmt = select(Bead).where(Bead.id == current)
            result = await sess.execute(stmt)
            bead = result.scalar_one_or_none()
            if not bead:
                break
            path.append(bead)
            current = bead.parent_id

        return list(reversed(path))

    async def diff_beads(
        self,
        bead_id1: str,
        bead_id2: str,
        session: Optional[AsyncSession] = None
    ) -> List[Dict[str, Any]]:
        """Compute structural diff between two beads."""
        sess = await self._get_session(session)

        stmt1 = select(Bead).where(Bead.id == bead_id1)
        stmt2 = select(Bead).where(Bead.id == bead_id2)
        result1 = await sess.execute(stmt1)
        result2 = await sess.execute(stmt2)
        bead1 = result1.scalar_one_or_none()
        bead2 = result2.scalar_one_or_none()

        if not bead1 or not bead2:
            raise ValueError("One or both beads not found")

        changes = []
        all_keys = set(bead2.content.keys()) | set(bead1.content.keys())

        for key in all_keys:
            val1 = bead1.content.get(key)
            val2 = bead2.content.get(key)
            if val1 != val2:
                changes.append({
                    "field": key,
                    "from": val1,
                    "to": val2
                })

        return changes

    async def list_branches(self, session: Optional[AsyncSession] = None) -> Dict[str, Dict[str, Any]]:
        """List all branches and their HEAD beads."""
        sess = await self._get_session(session)

        stmt = (
            select(Bead.branch_name, func.max(Bead.timestamp).label("max_ts"))
            .group_by(Bead.branch_name)
        )
        result = await sess.execute(stmt)
        branch_data = result.all()

        branches = {}
        for branch_name, max_ts in branch_data:
            bead_stmt = select(Bead).where(
                Bead.branch_name == branch_name,
                Bead.timestamp == max_ts
            )
            bead_result = await sess.execute(bead_stmt)
            head_bead = bead_result.scalar_one_or_none()
            if head_bead:
                branches[branch_name] = {
                    "head_id": head_bead.id,
                    "head_timestamp": head_bead.timestamp.isoformat(),
                    "head_action": head_bead.action.value
                }

        return branches
