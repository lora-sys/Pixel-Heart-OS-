"""
NPCService - Business logic for NPC generation and management.
"""
from typing import Optional, List, Dict, Any

from llm.service import LLMService
from infrastructure.database.repositories.character_repo import CharacterRepository
from infrastructure.database.repositories.relationship_repo import RelationshipRepository
from vector_store.chroma_client import ChromaClient


class NPCService:
    """Service for NPC-related operations."""

    def __init__(
        self,
        llm_service: LLMService,
        character_repo: CharacterRepository,
        chroma_client: ChromaClient
    ):
        self.llm_service = llm_service
        self.character_repo = character_repo
        self.chroma_client = chroma_client

    async def generate_npcs(
        self,
        heroine_soul: Dict[str, Any],
        roles: List[str] = ["protector", "competitor", "shadow"]
    ) -> List[Dict[str, Any]]:
        """
        Generate NPCs based on heroine's soul structure.

        Args:
            heroine_soul: Heroine's soul data
            roles: List of NPC roles to generate

        Returns:
            List of generated NPC data
        """
        npcs = []

        for role in roles:
            npc_data = await self.llm_service.generate_npc(heroine_soul, role)

            # Create character record
            npc_id = self._generate_npc_id(role)
            character_data = {
                "id": npc_id,
                "name": npc_data.get("identity", {}).get("name", role.capitalize()),
                "role": role,
                "soul_file_path": "",
                "identity_file_path": "",
                "voice_file_path": None,
                "cached_soul": npc_data.get("soul", {}),
                "cached_identity": npc_data.get("identity", {}),
                "cached_voice": npc_data.get("voice", {})
            }

            npc = await self.character_repo.create(character_data)

            # Store embedding for semantic retrieval
            await self._store_npc_embedding(npc, npc_data)

            npcs.append(self._character_to_dict(npc))

        return npcs

    async def get_npc(self, npc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve NPC by ID."""
        npc = await self.character_repo.get_by_id(npc_id)
        return self._character_to_dict(npc) if npc else None

    async def refine_npc(
        self,
        npc_id: str,
        feedback: str
    ) -> Dict[str, Any]:
        """
        Refine NPC based on user feedback.
        """
        npc = await self.character_repo.get_by_id(npc_id)
        if not npc:
            raise ValueError(f"NPC {npc_id} not found")

        # Use LLM to refine
        refined_data = await self.llm_service.refine_npc(
            {
                "soul": npc.cached_soul,
                "identity": npc.cached_identity,
                "voice": npc.cached_voice
            },
            feedback
        )

        # Update character
        updates = {
            "cached_soul": refined_data.get("soul", npc.cached_soul),
            "cached_identity": refined_data.get("identity", npc.cached_identity),
            "cached_voice": refined_data.get("voice", npc.cached_voice)
        }

        await self.character_repo.update(npc_id, updates)
        await self._update_npc_embedding(npc_id, refined_data)

        return await self.get_npc(npc_id)

    async def find_similar_npcs(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find NPCs semantically similar to query.
        Uses ChromaDB vector search.
        """
        results = await self.chroma_client.query(
            collection_name="npcs",
            query_texts=[query],
            n_results=limit
        )

        # Extract NPC IDs from results
        similar_npcs = []
        for result in results.get("ids", [[]])[0]:
            npc_id = result  # assuming collection stores npc_id as ID
            npc = await self.character_repo.get_by_id(npc_id)
            if npc:
                similar_npcs.append(self._character_to_dict(npc))

        return similar_npcs

    def _generate_npc_id(self, role: str) -> str:
        """Generate unique NPC ID."""
        import uuid
        return f"npc_{role}_{uuid.uuid4().hex[:12]}"

    async def _store_npc_embedding(
        self,
        npc,
        npc_data: Dict[str, Any]
    ) -> None:
        """Store NPC embedding in ChromaDB."""
        # Create searchable text from NPC data
        text = self._npc_to_text(npc_data)

        await self.chroma_client.add(
            collection_name="npcs",
            documents=[text],
            metadatas=[{"npc_id": npc.id, "role": npc.role}],
            ids=[npc.id]
        )

    async def _update_npc_embedding(
        self,
        npc_id: str,
        refined_data: Dict[str, Any]
    ) -> None:
        """Update existing NPC embedding."""
        text = self._npc_to_text(refined_data)

        await self.chroma_client.update(
            collection_name="npcs",
            ids=[npc_id],
            documents=[text]
        )

    def _npc_to_text(self, npc_data: Dict[str, Any]) -> str:
        """Convert NPC data to searchable text."""
        soul = npc_data.get("soul", {})
        identity = npc_data.get("identity", {})
        voice = npc_data.get("voice", {})

        parts = []
        if identity.get("name"):
            parts.append(f"Name: {identity['name']}")
        if identity.get("personality"):
            parts.append(f"Personality: {identity['personality']}")
        if identity.get("backstory"):
            parts.append(f"Backstory: {identity['backstory']}")
        if soul.get("key_traits"):
            parts.append(f"Traits: {', '.join(soul['key_traits'])}")
        if voice.get("emotional_tone", {}).get("primary"):
            parts.append(f"Emotional tone: {voice['emotional_tone']['primary']}")

        return " | ".join(parts)

    def _character_to_dict(self, character) -> Dict[str, Any]:
        """Convert Character model to API response dict."""
        return {
            "id": character.id,
            "name": character.name,
            "role": character.role,
            "soul": character.cached_soul,
            "identity": character.cached_identity,
            "voice": character.cached_voice,
            "created_at": character.created_at.isoformat() if hasattr(character, 'created_at') else None,
            "updated_at": character.updated_at.isoformat() if hasattr(character, 'updated_at') else None
        }

    async def list_npcs(self) -> List[Dict[str, Any]]:
        """List all NPCs (protector, competitor, shadow)."""
        all_characters = await self.character_repo.list_all()
        npcs = [c for c in all_characters if c.role in ["protector", "competitor", "shadow"]]
        return [self._character_to_dict(npc) for npc in npcs]
