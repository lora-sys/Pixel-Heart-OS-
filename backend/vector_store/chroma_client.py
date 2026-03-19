"""ChromaDB client wrapper for semantic conversation retrieval."""

import os
from typing import Optional, List, Dict, Any
import chromadb


class VectorStoreService:
    """Vector store service for semantic search operations."""

    def __init__(self, persist_directory: str = "./data/chroma"):
        """Initialize vector store service."""
        self._persist_directory = persist_directory
        self._client: Optional[chromadb.Client] = None
        self._collections: Dict[str, Any] = {}

    def _get_client(self) -> chromadb.Client:
        """Get or create ChromaDB client."""
        if self._client is None:
            self._client = chromadb.PersistentClient(path=self._persist_directory)
        return self._client

    async def ensure_collections(self) -> None:
        """Ensure required collections exist."""
        client = self._get_client()

        if "conversations" not in self._collections:
            self._collections["conversations"] = client.get_or_create_collection(
                name="conversations",
                metadata={"description": "NPC conversation memories"},
            )

        if "npc_backstories" not in self._collections:
            self._collections["npc_backstories"] = client.get_or_create_collection(
                name="npc_backstories",
                metadata={"description": "NPC backstory and personality memories"},
            )

    async def add_conversation(
        self,
        document: str,
        metadata: Dict[str, Any],
        conversation_id: Optional[str] = None,
    ) -> str:
        """Add conversation to vector store."""
        await self.ensure_collections()

        if conversation_id is None:
            import uuid

            conversation_id = f"conv_{uuid.uuid4().hex}"

        self._collections["conversations"].add(
            documents=[document],
            metadatas=[metadata],
            ids=[conversation_id],
        )
        return conversation_id

    async def search_conversations(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Search conversations using semantic similarity."""
        await self.ensure_collections()

        return self._collections["conversations"].query(
            query_texts=[query],
            n_results=n_results,
            where=filter_metadata,
            include=["documents", "metadatas", "distances"],
        )

    async def get_npc_backstories(
        self,
        npc_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get NPC backstories from vector store."""
        await self.ensure_collections()

        filter_metadata = {"npc_name": npc_name} if npc_name else None
        result = self._collections["npc_backstories"].get(
            where=filter_metadata,
            include=["documents", "metadatas"],
        )

        return (
            [
                {"document": doc, "metadata": meta}
                for doc, meta in zip(result["documents"], result["metadatas"])
            ]
            if result["documents"]
            else []
        )

    async def add_npc_backstory(
        self,
        npc_id: str,
        npc_name: str,
        backstory: str,
        archetype: str,
    ) -> str:
        """Add NPC backstory to vector store."""
        await self.ensure_collections()

        metadata = {
            "npc_id": npc_id,
            "npc_name": npc_name,
            "archetype": archetype,
        }

        self._collections["npc_backstories"].add(
            documents=[backstory],
            metadatas=[metadata],
            ids=[npc_id],
        )
        return npc_id
