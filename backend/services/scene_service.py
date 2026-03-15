"""
SceneService - Business logic for scene generation and management.
"""
from typing import Optional, List, Dict, Any

from llm.service import LLMService
from vector_store.chroma_client import ChromaClient
from database import Scene


class SceneService:
    """Service for scene-related operations."""

    def __init__(
        self,
        llm_service: LLMService,
        chroma_client: ChromaClient
    ):
        self.llm_service = llm_service
        self.chroma_client = chroma_client
        # Scene repository not needed if we store in files only?
        # Could also have SceneRepository if needed

    async def generate_scenes(
        self,
        heroine_preferences: List[str],
        count: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Generate scenes based on heroine's preferences.

        Args:
            heroine_preferences: List of scene type preferences
            count: Number of scenes to generate

        Returns:
            List of scene data dictionaries
        """
        scenes = []

        for _ in range(count):
            scene_data = await self.llm_service.generate_scene(heroine_preferences)

            # Create scene record
            scene_id = self._generate_scene_id()
            scene_dict = {
                "id": scene_id,
                "name": scene_data.get("name", "Untitled Scene"),
                "description": scene_data.get("description", ""),
                "config": scene_data,
                "image_path": None
            }
            scenes.append(scene_dict)

            # Store in vector store for later retrieval
            await self._store_scene_embedding(scene_id, scene_data)

        return scenes

    async def find_similar_scenes(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find scenes semantically similar to query.
        """
        results = await self.chroma_client.query(
            collection_name="scenes",
            query_texts=[query],
            n_results=limit
        )

        # For now, return raw metadata
        scenes = []
        for i, scene_id in enumerate(results.get("ids", [[]])[0]):
            metadata = results.get("metadatas", [[]])[0][i] if results.get("metadatas") else {}
            scenes.append({
                "id": scene_id,
                "metadata": metadata
            })

        return scenes

    def _generate_scene_id(self) -> str:
        """Generate unique scene ID."""
        import uuid
        return f"scene_{uuid.uuid4().hex[:12]}"

    async def _store_scene_embedding(
        self,
        scene_id: str,
        scene_data: Dict[str, Any]
    ) -> None:
        """Store scene embedding in ChromaDB."""
        text = self._scene_to_text(scene_data)

        await self.chroma_client.add(
            collection_name="scenes",
            documents=[text],
            metadatas=[{"scene_id": scene_id}],
            ids=[scene_id]
        )

    def _scene_to_text(self, scene_data: Dict[str, Any]) -> str:
        """Convert scene data to searchable text."""
        parts = []
        parts.append(f"Name: {scene_data.get('name', '')}")
        parts.append(f"Description: {scene_data.get('description', '')}")
        parts.append(f"Mood: {scene_data.get('mood', '')}")
        parts.append(f"Location: {scene_data.get('environment', {}).get('location_type', '')}")
        parts.append(f"Time: {scene_data.get('environment', {}).get('time_of_day', '')}")
        parts.append(f"Weather: {scene_data.get('environment', {}).get('weather', '')}")

        triggers = scene_data.get('triggers', [])
        if triggers:
            parts.append(f"Triggers: {', '.join(triggers)}")

        return " | ".join(parts)
