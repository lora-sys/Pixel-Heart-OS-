"""
Simulation Service for running turn-based conversations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class SimulationService:
    """Service for running LangGraph simulation workflow."""

    def __init__(self):
        """Initialize SimulationService."""
        self._state: Dict[str, Any] = {}
        self._conversation_history: List[Dict[str, Any]] = []

    async def run_turn(
        self,
        heroine_data: Dict[str, Any],
        npcs: List[Dict[str, Any]],
        player_action: str,
    ) -> Dict[str, Any]:
        """Run a simulation turn."""
        responses = []
        for npc in npcs:
            response = {
                "npc_id": npc["id"],
                "npc_name": npc.get("name", "Unknown"),
                "message": f"Response from {npc.get('archetype', 'Character')}",
                "emotion": "neutral",
            }
            responses.append(response)

        conversation_entry = {
            "player_action": player_action,
            "npc_responses": responses,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._conversation_history.append(conversation_entry)

        result = {
            "turn_number": len(self._conversation_history),
            "player_action": player_action,
            "npc_responses": responses,
            "relationships": {npc["id"]: 0.1 for npc in npcs},
            "new_bead_id": f"bead_{len(self._conversation_history)}",
        }
        return result

    async def reset(self) -> Dict[str, str]:
        """Reset simulation state."""
        self._state = {}
        self._conversation_history = []
        return {"status": "reset"}

    async def get_history(self) -> List[Dict[str, Any]]:
        """Get conversation history."""
        return self._conversation_history
