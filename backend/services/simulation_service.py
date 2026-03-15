"""
SimulationService - Business logic for simulation/turn-based interactions.
"""
from typing import Optional, Dict, Any, List
from datetime import datetime

from llm.service import LLMService
from services.bead_service import BeadService
from infrastructure.database.repositories.relationship_repo import RelationshipRepository
from infrastructure.database.repositories.character_repo import CharacterRepository
from database import Bead, ActionType, EmotionTag


class SimulationService:
    """
    Service for managing simulation turns.
    Orchestrates NPC responses and state updates.
    """

    def __init__(
        self,
        llm_service: LLMService,
        bead_service: BeadService,
        relationship_repo: RelationshipRepository,
        character_repo: CharacterRepository
    ):
        self.llm_service = llm_service
        self.bead_service = bead_service
        self.relationship_repo = relationship_repo
        self.character_repo = character_repo

    async def process_turn(
        self,
        player_action: str,
        current_bead_id: Optional[str],
        branch_name: str = "main",
        context_length: int = 5
    ) -> Dict[str, Any]:
        """
        Process a player's turn in the simulation.

        Args:
            player_action: Player's dialogue/action
            current_bead_id: Current narrative state (bead)
            branch_name: Branch to operate on
            context_length: Number of previous beads to include as context

        Returns:
            Simulation result with NPC responses and new bead
        """
        # Get timeline context
        timeline = await self.bead_service.get_timeline(
            branch_name=branch_name,
            limit=context_length
        )

        # Build context string from timeline
        context = self._build_context(timeline)

        # Determine which NPCs are present in current scene
        # For now, get all NPCs (protector, competitor, shadow)
        npcs = await self.character_repo.list_all()
        present_npcs = [n for n in npcs if n.role in ["protector", "competitor", "shadow"]]

        # Generate responses from each NPC
        npc_responses = []
        for npc in present_npcs:
            response = await self.llm_service.simulate_npc_response(
                npc=self._character_to_dict(npc),
                context=context,
                player_action=player_action
            )

            # Determine emotion tag from response
            emotion = response.get("emotion", "neutral").lower()

            # Record this interaction as a bead
            bead_content = {
                "player_action": player_action,
                "npc_name": npc.name,
                "npc_id": npc.id,
                "dialogue": response.get("dialogue", ""),
                "emotion": emotion,
                "relationship_delta": response.get("relationship_delta", 0.0)
            }

            bead = await self.bead_service.create_bead(
                action="npc_interaction",
                content=bead_content,
                parent_id=current_bead_id,
                branch_name=branch_name,
                emotion_tag=emotion if emotion in self._get_valid_emotions() else None
            )

            # Update relationship scores
            await self._update_relationship(
                character_id=npc.id,
                target_character_id="heroine",  # TODO: get actual heroine ID
                delta=response.get("relationship_delta", 0.0)
            )

            npc_responses.append({
                "npc_id": npc.id,
                "npc_name": npc.name,
                "dialogue": response.get("dialogue", ""),
                "emotion": emotion,
                "relationship_delta": response.get("relationship_delta", 0.0),
                "bead_id": bead["id"]
            })

        # Create a summary bead representing the turn
        turn_bead = await self.bead_service.create_bead(
            action="turn",
            content={
                "player_action": player_action,
                "npc_count": len(npc_responses),
                "npc_responses": [r["npc_id"] for r in npc_responses]
            },
            parent_id=current_bead_id,
            branch_name=branch_name,
            emotion_tag=self._aggregate_emotion(npc_responses)
        )

        return {
            "turn_bead_id": turn_bead["id"],
            "npc_responses": npc_responses,
            "branch_name": branch_name,
            "timestamp": turn_bead["timestamp"]
        }

    async def get_simulation_state(
        self,
        branch_name: str = "main"
    ) -> Dict[str, Any]:
        """
        Get current simulation state.
        Returns dict matching SimulationStateResponse schema.
        """
        head_bead = await self.bead_service.get_head(branch_name)

        # Get heroine
        heroine = await self.character_repo.get_first_by_role("heroine")
        heroine_id = heroine.id if heroine else None

        # Get all active NPCs (filter by role)
        all_characters = await self.character_repo.list_all()
        active_npcs = [c for c in all_characters if c.role in ["protector", "competitor", "shadow"]]

        # Build active_npcs list matching NPCResponse schema
        active_npc_dicts = []
        for npc in active_npcs:
            active_npc_dicts.append({
                "id": npc.id,
                "name": npc.name,
                "role": npc.role,
                "relationship_to_heroine": npc.role,
                "soul": npc.cached_soul,
                "identity": npc.cached_identity,
                "voice": npc.cached_voice,
                "created_at": npc.created_at
            })

        # Build relationships: heroine_id -> npc_id trust score
        relationships = {}
        if heroine_id:
            for npc in active_npcs:
                rel = await self.relationship_repo.get_by_pair(heroine_id, npc.id)
                relationships[npc.id] = rel.trust_score if rel else 0.0

        # Get available branches
        branches_data = await self.bead_service.list_branches()
        available_branches = list(branches_data.keys())

        # Current scene: for now, None (could be loaded from bead content or scene service)
        current_scene = None

        return {
            "current_scene": current_scene,
            "active_npcs": active_npc_dicts,
            "relationships": relationships,
            "current_bead_id": head_bead["id"] if head_bead else None,
            "available_branches": available_branches
        }

    def _build_context(self, timeline: List[Dict[str, Any]]) -> str:
        """Build conversation context from timeline."""
        if not timeline:
            return ""

        lines = ["Recent narrative timeline:"]
        for bead in timeline[-10:]:  # Last 10 beads
            action = bead.get("action", "")
            content = bead.get("content", {})
            if action == "turn":
                player_action = content.get("player_action", "")
                lines.append(f"Player: {player_action}")
            elif action == "npc_interaction":
                npc_name = content.get("npc_name", "")
                dialogue = content.get("dialogue", "")
                lines.append(f"{npc_name}: {dialogue}")

        return "\n".join(lines)

    async def _update_relationship(
        self,
        character_id: str,
        target_character_id: str,
        delta: float
    ) -> None:
        """
        Update relationship score between characters.
        Delta is cumulative (positive or negative).
        """
        relationship = await self.relationship_repo.get_by_pair(
            character_id=character_id,
            target_character_id=target_character_id
        )

        if relationship:
            # Update trust_score (clamped -1.0 to 1.0)
            new_trust = relationship.trust_score + delta
            new_trust = max(-1.0, min(1.0, new_trust))

            await self.relationship_repo.update_scores(
                character_id=character_id,
                target_character_id=target_character_id,
                trust_score=new_trust,
                append_history=f"Turn delta: {delta}"
            )

    def _aggregate_emotion(self, npc_responses: List[Dict[str, Any]]) -> str:
        """Aggregate emotion from multiple NPC responses."""
        if not npc_responses:
            return "neutral"

        # Simple majority vote or prioritize strong emotions
        emotions = [r["emotion"] for r in npc_responses]
        # Return most common emotion
        from collections import Counter
        return Counter(emotions).most_common(1)[0][0]

    def _get_valid_emotions(self) -> List[str]:
        """Get list of valid emotion tag values."""
        from database import EmotionTag
        return [e.value for e in EmotionTag]

    def _character_to_dict(self, character) -> Dict[str, Any]:
        """Convert Character model to dictionary."""
        return {
            "id": character.id,
            "name": character.name,
            "role": character.role,
            "soul": character.cached_soul,
            "identity": character.cached_identity,
            "voice": character.cached_voice
        }
