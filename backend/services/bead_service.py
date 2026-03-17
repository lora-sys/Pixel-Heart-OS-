"""
Bead Service for managing Beads (DAG nodes).
"""

from typing import Dict, List, Optional, Any
import hashlib
from datetime import datetime


class BeadService:
    """Service for managing beads in the narrative DAG."""

    def __init__(self):
        """Initialize BeadService."""
        self._beads: Dict[str, Dict[str, Any]] = {}

    async def create_bead(
        self,
        parent_id: Optional[str],
        content: Dict[str, Any],
        action: str,
        branch_name: str = "main",
        emotion_tag: Optional[str] = None,
    ) -> str:
        """Create a new bead in the DAG."""
        bead_data = {
            "parent_id": parent_id,
            "content": content,
            "action": action,
            "branch_name": branch_name,
            "emotion_tag": emotion_tag,
            "timestamp": datetime.utcnow().isoformat(),
        }
        bead_id = hashlib.sha1(str(bead_data).encode()).hexdigest()[:40]
        bead_data["id"] = bead_id
        self._beads[bead_id] = bead_data
        return bead_id

    async def get_bead(self, bead_id: str) -> Optional[Dict[str, Any]]:
        """Get a bead by ID."""
        return self._beads.get(bead_id)

    async def get_timeline(
        self, branch_name: str = "main", limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get timeline for a branch."""
        beads = [b for b in self._beads.values() if b.get("branch_name") == branch_name]
        beads.sort(key=lambda x: x.get("timestamp", ""))
        return beads[:limit]

    async def create_branch(self, branch_name: str, from_bead_id: str) -> str:
        """Create a new branch from an existing bead."""
        return f"branch_{branch_name}_{from_bead_id[:8]}"

    async def merge_branches(self, source_branch: str, target_branch: str) -> str:
        """Merge two branches."""
        return hashlib.sha1(
            f"merge_{source_branch}_{target_branch}".encode()
        ).hexdigest()[:40]
