"""
Scene Service for generating and managing scenes.
"""

from typing import Dict, List, Optional, Any
import hashlib
from datetime import datetime


class SceneService:
    """Service for generating and managing scenes."""

    def __init__(self):
        """Initialize SceneService."""
        self._scenes: Dict[str, Dict[str, Any]] = {}

    async def generate_scene(
        self, heroine: Dict[str, Any], npcs: List[Dict[str, Any]], context: str = ""
    ) -> Dict[str, Any]:
        """Generate a scene based on heroine and NPCs."""
        scene_id = hashlib.md5(
            f"{heroine.get('identity', {}).get('name', 'heroine')}_{len(npcs)}_{context}".encode()
        ).hexdigest()[:8]

        scene = {
            "id": scene_id,
            "title": f"Scene at {context or 'Unknown Location'}",
            "location": context or "Mysterious Place",
            "npc_ids": [npc["id"] for npc in npcs],
            "atmosphere": self._determine_atmosphere(npcs),
            "description": f"The heroine meets {len(npcs)} characters in {context or 'a mysterious place'}.",
            "created_at": datetime.utcnow().isoformat(),
        }
        self._scenes[scene_id] = scene
        return scene

    def _determine_atmosphere(self, npcs: List[Dict[str, Any]]) -> str:
        if not npcs:
            return "neutral"
        archetypes = [npc.get("archetype", "") for npc in npcs]
        if "Shadow" in archetypes or "Competitor" in archetypes:
            return "tense"
        if "Ally" in archetypes or "Mentor" in archetypes:
            return "warm"
        return "mysterious"

    async def get_scenes(self) -> List[Dict[str, Any]]:
        """Get all scenes."""
        return list(self._scenes.values())
