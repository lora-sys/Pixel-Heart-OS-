"""
Beads Engine: Git-like DAG narrative state management.
"""
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, and_
import hashlib
import json

from database import Bead, get_session, ActionType, EmotionTag


class BeadEngine:
    """
    Core engine for managing Beads DAG.
    Provides branching, merging, rebasing, and timeline traversal.
    """

    def __init__(self):
        self._session: Optional[AsyncSession] = None

    async def _get_session(self) -> AsyncSession:
        """Get or create database session."""
        if self._session is None:
            # Create new session from factory
            self._session = await anext(get_session())
        return self._session

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
        signature: Optional[str] = None
    ) -> Bead:
        """
        Create a new Bead and attach it to the DAG.
        Validates DAG structure (no cycles).
        """
        session = await self._get_session()

        # Validate parent exists (if provided)
        if parent_id:
            stmt = select(Bead).where(Bead.id == parent_id)
            result = await session.execute(stmt)
            parent = result.scalar_one_or_none()
            if not parent:
                raise ValueError(f"Parent bead {parent_id} not found")

            # Check that adding this child doesn't create a cycle
            if await self._would_create_cycle(parent_id, parent.branch_name, branch_name):
                raise ValueError("Adding this bead would create a cycle in the DAG")

        # Calculate bead ID
        bead_id = await self._sha1_hash(parent_id, content, action)

        # Check for duplicate ID (extremely unlikely but safe)
        existing = await session.execute(select(Bead).where(Bead.id == bead_id))
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

        session.add(bead)
        await session.flush()

        # Update branch HEAD (store in beads table with special marker or separate table)
        # For simplicity, we rely on querying max timestamp per branch

        await session.commit()
        await session.refresh(bead)

        return bead

    async def _would_create_cycle(self, start_id: str, start_branch: str, target_branch: str) -> bool:
        """
        Check if adding a bead with parent_id=start_id to target_branch
        would create a cycle (i.e., target_branch already reaches start_id).
        """
        session = await self._get_session()

        # If target_branch == start_branch, cannot add child that is already an ancestor
        if target_branch == start_branch:
            # Walk up from start_id to see if we encounter a bead already on target_branch
            current_id = start_id
            while current_id:
                stmt = select(Bead).where(Bead.id == current_id)
                result = await session.execute(stmt)
                current = result.scalar_one_or_none()
                if not current:
                    break
                # Check if any ancestor is already on target_branch
                # Actually we need to check if current bead's branch is target_branch
                # But in DAG, a bead belongs to only one branch
                if current.branch_name == target_branch and current_id != start_id:
                    return True
                current_id = current.parent_id

        return False

    async def get_timeline(
        self,
        branch_name: str = "main",
        limit: Optional[int] = None
    ) -> List[Bead]:
        """
        Get timeline (ancestors + descendants in chronological order) for a branch.
        """
        session = await self._get_session()

        # Get all beads on this branch
        stmt = select(Bead).where(
            Bead.branch_name == branch_name
        ).order_by(Bead.timestamp.asc())

        if limit:
            stmt = stmt.limit(limit)

        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_head(self, branch_name: str = "main") -> Optional[Bead]:
        """Get HEAD (latest bead) for a branch."""
        beads = await self.get_timeline(branch_name)
        return beads[-1] if beads else None

    async def get_branch_point(self, bead_id1: str, bead_id2: str) -> Optional[Bead]:
        """
        Find the common ancestor (merge base) of two beads.
        """
        session = await self._get_session()

        # Get ancestors of bead1
        ancestors1 = set()
        current = bead_id1
        while current:
            ancestors1.add(current)
            stmt = select(Bead).where(Bead.id == current)
            result = await session.execute(stmt)
            bead = result.scalar_one_or_none()
            if not bead:
                break
            current = bead.parent_id

        # Walk up from bead2 to find first common ancestor
        current = bead_id2
        while current:
            if current in ancestors1:
                stmt = select(Bead).where(Bead.id == current)
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
            stmt = select(Bead).where(Bead.id == current)
            result = await session.execute(stmt)
            bead = result.scalar_one_or_none()
            if not bead:
                break
            current = bead.parent_id

        return None

    async def create_branch(
        self,
        branch_name: str,
        from_bead_id: str
    ) -> Tuple[str, Bead]:
        """
        Create a new branch starting from a given bead.
        Returns (branch_name, HEAD bead).
        """
        session = await self._get_session()

        # Validate source bead exists
        stmt = select(Bead).where(Bead.id == from_bead_id)
        result = await session.execute(stmt)
        from_bead = result.scalar_one_or_none()
        if not from_bead:
            raise ValueError(f"Source bead {from_bead_id} not found")

        # Check if branch already exists
        existing_head = await self.get_head(branch_name)
        if existing_head:
            raise ValueError(f"Branch '{branch_name}' already exists")

        # Branching is implicit - just note that the branch starts at from_bead
        # Future beads will set branch_name=branch_name
        # For auditability, we could create a special "branch" bead

        return branch_name, from_bead

    async def merge_branches(
        self,
        source_branch: str,
        target_branch: str,
        strategy: str = "auto"
    ) -> Bead:
        """
        Merge source branch into target branch.
        Creates a merge bead with both parents.
        Strategy: "auto" (LLM-assisted), "ours", "theirs", "fast-forward only"
        """
        session = await self._get_session()

        source_head = await self.get_head(source_branch)
        target_head = await self.get_head(target_branch)

        if not source_head:
            raise ValueError(f"Source branch '{source_branch}' is empty")
        if not target_head:
            # Target empty: just move HEAD
            source_head.branch_name = target_branch
            await session.commit()
            return source_head

        # Check if fast-forward possible
        if await self._is_ancestor(source_head.id, target_head.id):
            # source HEAD is ahead of target HEAD - fast forward
            # Update all beads from source HEAD to target branch (expensive but correct)
            # Alternative: just set new bead as merge point
            # Simpler: create merge bead anyway
            pass

        # Create merge bead with dual parents
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
            parent_id=target_head.id,  # Primary parent is target
            branch_name=target_branch,
            emotion_tag="neutral"
        )

        # In full implementation, would also mark source branch's HEAD as merged
        # or create a synthetic bead linking source to merge point

        return merge_bead

    async def _is_ancestor(self, candidate_id: str, descendant_id: str) -> bool:
        """Check if candidate is an ancestor of descendant."""
        session = await self._get_session()

        current = descendant_id
        while current:
            if current == candidate_id:
                return True
            stmt = select(Bead).where(Bead.id == current)
            result = await session.execute(stmt)
            bead = result.scalar_one_or_none()
            if not bead:
                break
            current = bead.parent_id

        return False

    async def rebase_branch(
        self,
        branch_name: str,
        onto_bead_id: str
    ) -> List[Bead]:
        """
        Rebase branch onto new base.
        Returns list of new rebased beads.
        """
        session = await self._get_session()

        branch_head = await self.get_head(branch_name)
        if not branch_head:
            raise ValueError(f"Branch '{branch_name}' is empty")

        # Verify onto_bead exists
        stmt = select(Bead).where(Bead.id == onto_bead_id)
        result = await session.execute(stmt)
        onto_bead = result.scalar_one_or_none()
        if not onto_bead:
            raise ValueError(f"Base bead {onto_bead_id} not found")

        # Get branch's unique commits (excluding common ancestor)
        common_ancestor = await self.get_branch_point(branch_head.id, onto_bead_id)
        if not common_ancestor:
            raise ValueError("No common ancestor found")

        # Collect commits to reapply
        commits = await self._collect_commits_after(common_ancestor.id, branch_head.id)

        # Reapply each commit onto onto_bead
        new_beads = []
        current_parent_id = onto_bead_id

        for commit in reversed(commits):  # oldest first
            new_bead = await self.create_bead(
                action=commit.action,
                content=commit.content,
                parent_id=current_parent_id,
                branch_name=branch_name,
                emotion_tag=commit.emotion_tag,
                signature=commit.signature
            )
            new_beads.append(new_bead)
            current_parent_id = new_bead.id

        return new_beads

    async def _collect_commits_after(
        self,
        ancestor_id: str,
        descendant_id: str
    ) -> List[Bead]:
        """Collect commits from ancestor (exclusive) to descendant (inclusive)."""
        session = await self._get_session()

        # Build path from descendant back to ancestor
        path = []
        current = descendant_id
        while current and current != ancestor_id:
            stmt = select(Bead).where(Bead.id == current)
            result = await session.execute(stmt)
            bead = result.scalar_one_or_none()
            if not bead:
                break
            path.append(bead)
            current = bead.parent_id

        return list(reversed(path))  # chronological order

    async def diff_beads(
        self,
        bead_id1: str,
        bead_id2: str
    ) -> List[Dict[str, Any]]:
        """
        Compute structural diff between two beads.
        Returns list of field changes.
        """
        session = await self._get_session()

        stmt1 = select(Bead).where(Bead.id == bead_id1)
        stmt2 = select(Bead).where(Bead.id == bead_id2)
        result1 = await session.execute(stmt1)
        result2 = await session.execute(stmt2)
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

    async def commit_bead(
        self,
        data: Dict[str, Any]
    ) -> Bead:
        """
        High-level helper: create bead and update HEAD atomically.
        """
        action = data["action"]
        content = data["content"]
        parent_id = data.get("parent_id")
        branch_name = data.get("branch_name", "main")
        emotion_tag = data.get("emotion_tag")

        return await self.create_bead(
            action=action,
            content=content,
            parent_id=parent_id,
            branch_name=branch_name,
            emotion_tag=emotion_tag,
            signature=data.get("signature")
        )

    async def list_branches(self) -> Dict[str, Dict[str, Any]]:
        """
        List all branches and their HEAD beads.
        """
        session = await self._get_session()

        # Get distinct branch names
        stmt = select(Bead.branch_name).distinct()
        result = await session.execute(stmt)
        branch_names = [row[0] for row in result.all()]

        branches = {}
        for branch in branch_names:
            head = await self.get_head(branch)
            if head:
                branches[branch] = {
                    "head_id": head.id,
                    "head_timestamp": head.timestamp.isoformat(),
                    "head_action": head.action.value
                }

        return branches
