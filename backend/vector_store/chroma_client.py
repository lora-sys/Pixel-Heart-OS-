"""
ChromaDB vector store for semantic memory retrieval.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
import uuid


class ChromaClient:
    """
    Wrapper for ChromaDB client with collection management.
    """

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="conversations",
            metadata={"hnsw:space": "cosine"}
        )

    def add_conversation(
        self,
        bead_id: str,
        text: str,
        metadata: Dict[str, Any] = {}
    ):
        """
        Add a conversation turn to the vector store.
        Chroma will automatically generate embeddings (using default all-MiniLM-L6-v2).
        """
        self.collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            metadatas=[{**metadata, "bead_id": bead_id}]
        )

    def search_conversations(
        self,
        query: str,
        k: int = 5,
        where: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for relevant past conversations.
        Returns list of {id, document, metadata, distance}.
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=where,
            include=["documents", "metadatas", "distances"]
        )

        formatted = []
        for i in range(len(results['ids'][0])):
            formatted.append({
                "id": results['ids'][0][i],
                "content": results['documents'][0][i],
                "metadata": results['metadatas'][0][i],
                "distance": results['distances'][0][i]
            })

        return formatted

    def clear(self):
        """Delete all data (for testing)."""
        self.client.reset()
