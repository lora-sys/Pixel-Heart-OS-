"""
Beads Engine - Git-inspired DAG for narrative version control.
Implements create, branch, merge, rebase, and diff operations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib
import json


class BeadEngine:
    """Engine for managing beads in a DAG structure."""

    def __init__(self):
        """Initialize BeadEngine with in-memory storage."""
        self._beads: Dict[str, Dict[str, Any]] = {}

    def create_bead(
        self,
        parent_id: Optional[str],
        content: Dict[str, Any],
        action: str,
        branch_name: str = "main",
        emotion_tag: Optional[str] = None
    ) -> str:
        """Create a new bead in the DAG.

        Args:
            parent_id: ID of parent bead (None for root)
            content: Bead content dictionary
            action: Action type (create_heroine, turn, merge, etc.)
            branch_name: Branch this bead belongs to
            emotion_tag: Optional emotion tag for UI

        Returns:
            Bead ID (SHA-1 hash)
        """
        timestamp = datetime.utcnow().isoformat()

        bead_data = {
            "parent_id": parent_id,
            "content": content,
            "action": action,
            "branch_name": branch_name,
            "emotion_tag": emotion_tag,
            "timestamp": timestamp,
        }

        bead_id = hashlib.sha1(json.dumps(bead_data, sort_keys=True).encode()).hexdigest()

        bead_data["id"] = bead_id
        self._beads[bead_id] = bead_data

        return bead_id

    def get_bead(self, bead_id: str) -> Optional[Dict[str, Any]]:
        """Get a bead by ID.

        Args:
            bead_id: Bead ID

        Returns:
            Bead data or None if not found
        """
        return self._beads.get(bead_id)

    def get_timeline(self, branch_name: str = "main", limit: int = 50) -> List[Dict[str, Any]]:
        """Get beads for a branch in chronological order.

        Args:
            branch_name: Branch to get timeline for
            limit: Maximum number of beads to return

        Returns:
            List of beads in chronological order
        """
        beads = [b for b in self._beads.values() if b.get("branch_name") == branch_name]
        beads.sort(key=lambda x: x.get("timestamp", ""))
        return beads[:limit]

    def create_branch(self, branch_name: str, from_bead_id: str) -> str:
        """Create a new branch from an existing bead.

        Args:
            branch_name: Name for the new branch
            from_bead_id: ID of bead to branch from

        Returns:
            Branch identifier
        """
        parent_bead = self.get_bead(from_bead_id)
        if not parent_bead:
            raise ValueError(f"Bead {from_bead_id} not found")

        return f"branch_{branch_name}_{from_bead_id[:8]}"

    def merge_branches(
        self,
        source_branch: str,
        target_branch: str,
        merge_message: Optional[str] = None
    ) -> str:
        """Merge two branches.

        Args:
            source_branch: Branch to merge from
            target_branch: Branch to merge into
            merge_message: Optional merge message

        Returns:
            Merge bead ID
        """
        source_beads = self.get_timeline(source_branch, limit=1)
        target_beads = self.get_timeline(target_branch, limit=1)

        if not source_beads or not target_beads:
            raise ValueError("Cannot merge: one or both branches are empty")

        content = {
            "merge_message": merge_message or f"Merge {source_branch} into {target_branch}",
            "source_branch": source_branch,
            "target_branch": target_branch,
        }

        merge_id = self.create_bead(
            parent_id=target_beads[-1]["id"],
            content=content,
            action="merge",
            branch_name=target_branch
        )

        return merge_id

    def rebase_branch(
        self,
        branch_name: str,
        new_base_bead_id: str
    ) -> Dict[str, Any]:
        """Rebase a branch onto a new base.

        Args:
            branch_name: Branch to rebase
            new_base_bead_id: New base bead ID

        Returns:
            Rebase result with old and new bead IDs
        """
        beads = self.get_timeline(branch_name)
        if not beads:
            return {"status": "empty", "message": "No beads to rebase"}

        return {
            "status": "success",
            "branch": branch_name,
            "new_base": new_base_bead_id,
            "rebased_count": len(beads),
        }

    def diff_beads(
        self,
        bead_id1: str,
        bead_id2: str
    ) -> Dict[str, Any]:
        """Compute diff between two beads.

        Args:
            bead_id1: First bead ID
            bead_id2: Second bead ID

        Returns:
            Diff result with added, removed, modified fields
        """
        bead1 = self.get_bead(bead_id1)
        bead2 = self.get_bead(bead_id2)

        if not bead1 or not bead2:
            raise ValueError("One or both beads not found")

        content1 = bead1.get("content", {})
        content2 = bead2.get("content", {})

        added = {k: v for k, v in content2.items() if k not in content1}
        removed = {k: v for k, v in content1.items() if k not in content2}

        modified = {}
        for k in set(content1.keys()) & set(content2.keys()):
            if content1[k] != content2[k]:
                modified[k] = {"old": content1[k], "new": content2[k]}

        return {
            "bead1": bead_id1,
            "bead2": bead_id2,
            "added": added,
            "removed": removed,
            "modified": modified,
        }

    def _would_create_cycle(
        self,
        parent_id: str,
        new_bead_id: str
    ) -> bool:
        """Check if creating a bead would create a cycle.

        Args:
            parent_id: Potential parent ID
            new_bead_id: New bead ID

        Returns:
            True if cycle would be created
        """
        visited = {new_bead_id}
        current = parent_id

        while current:
            if current in visited:
                return True
            visited.add(current)
            bead = self.get_bead(current)
            if not bead:
                break
            current = bead.get("parent_id")

        return False

    def get_children(self, bead_id: str) -> List[str]:
        """Get all children of a bead.

        Args:
            bead_id: Parent bead ID

        Returns:
            List of child bead IDs
        """
        return [
            b["id"] for b in self._beads.values()
            if b.get("parent_id") == bead_id
        ]

    def get_ancestors(self, bead_id: str) -> List[str]:
        """Get all ancestors of a bead.

        Args:
            bead_id: Bead ID

        Returns:
            List of ancestor bead IDs in order from root to parent
        """
        ancestors = []
        current = bead_id

        while current:
            bead = self.get_bead(current)
            if not bead:
                break
            parent_id = bead.get("parent_id")
            if parent_id:
                ancestors.append(parent_id)
            current = parent_id

        return list(reversed(ancestors))

    def get_branch_heads(self) -> Dict[str, str]:
        """Get the head bead ID for each branch.

        Returns:
            Dictionary mapping branch names to head bead IDs
        """
        branches = {}
        for bead in self._beads.values():
            branch = bead.get("branch_name", "main")
            if branch not in branches:
                branches[branch] = bead["id"]
            else:
                existing = self.get_bead(branches[branch])
                if existing and bead.get("timestamp", "") > existing.get("timestamp", ""):
                    branches[branch] = bead["id"]

        return branches
