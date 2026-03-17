"""
NPC Service for generating and managing NPCs.
"""

from typing import Dict, List, Optional, Any
import hashlib
from datetime import datetime


class NPCService:
    """Service for generating and managing NPCs."""

    def __init__(self):
        """Initialize NPCService."""
        self._npcs: Dict[str, Dict[str, Any]] = {}

    async def generate_npcs(
        self, heroine_data: Dict[str, Any], count: int = 3
    ) -> List[Dict[str, Any]]:
        """Generate NPCs based on heroine data."""
        npcs = []
        archetypes = ["Protector", "Competitor", "Shadow", "Ally", "Mentor"]

        for i in range(count):
            archetype = archetypes[i % len(archetypes)]
            npc_id = hashlib.md5(
                f"{heroine_data.get('identity', {}).get('name', 'heroine')}_{archetype}_{i}".encode()
            ).hexdigest()[:8]

            npc = {
                "id": npc_id,
                "name": f"{archetype}_{i + 1}",
                "archetype": archetype,
                "role": self._get_role_for_archetype(archetype),
                "personality": self._generate_personality(archetype),
                "relationship": 0.0,
                "created_at": datetime.utcnow().isoformat(),
            }
            npcs.append(npc)
            self._npcs[npc_id] = npc

        return npcs

    def _get_role_for_archetype(self, archetype: str) -> str:
        roles = {
            "Protector": "Guardian",
            "Competitor": "Rival",
            "Shadow": "Antagonist",
            "Ally": "Friend",
            "Mentor": "Guide",
        }
        return roles.get(archetype, "Character")

    def _generate_personality(self, archetype: str) -> Dict[str, str]:
        personalities = {
            "Protector": {"trait1": "brave", "trait2": "loyal", "trait3": "protective"},
            "Competitor": {
                "trait1": "ambitious",
                "trait2": "driven",
                "trait3": "competitive",
            },
            "Shadow": {
                "trait1": "mysterious",
                "trait2": "enigmatic",
                "trait3": "secretive",
            },
            "Ally": {"trait1": "kind", "trait2": "supportive", "trait3": "trustworthy"},
            "Mentor": {"trait1": "wise", "trait2": "experienced", "trait3": "patient"},
        }
        return personalities.get(archetype, {"trait1": "neutral"})

    async def get_npcs(self) -> List[Dict[str, Any]]:
        """Get all NPCs."""
        return list(self._npcs.values())

    async def update_npc(
        self, npc_id: str, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update an NPC."""
        if npc_id in self._npcs:
            self._npcs[npc_id].update(updates)
            return self._npcs[npc_id]
        return None
