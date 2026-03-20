"""
Container for dependency injection.
"""

from typing import Dict, Any
from llm.service import LLMService
from beads.engine import BeadEngine
from storage.file_system import FileSystemService


class Container:
    """Dependency injection container for services."""

    def __init__(self):
        """Initialize container."""
        self._singletons: Dict[str, Any] = {}

    def get_llm_service(self) -> LLMService:
        """Get LLM service singleton."""
        if "llm_service" not in self._singletons:
            self._singletons["llm_service"] = LLMService()
        return self._singletons["llm_service"]

    def get_bead_engine(self) -> BeadEngine:
        """Get BeadEngine singleton."""
        if "bead_engine" not in self._singletons:
            self._singletons["bead_engine"] = BeadEngine()
        return self._singletons["bead_engine"]

    def get_storage_service(self) -> FileSystemService:
        """Get FileSystemService singleton."""
        if "storage_service" not in self._singletons:
            self._singletons["storage_service"] = FileSystemService()
        return self._singletons["storage_service"]

    def get_vector_store(self) -> Any:
        """Get VectorStoreService singleton."""
        if "vector_store" not in self._singletons:
            from vector_store.chroma_client import VectorStoreService

            self._singletons["vector_store"] = VectorStoreService()
        return self._singletons["vector_store"]

    def get_heroine_service(self) -> Any:
        """Get HeroineService singleton."""
        if "heroine_service" not in self._singletons:
            from services.heroine_service import HeroineService
            from services.bead_service import BeadService

            bead_service = BeadService()
            self._singletons["heroine_service"] = HeroineService(
                llm_service=self.get_llm_service(),
                storage_service=self.get_storage_service(),
                bead_service=bead_service,
            )
        return self._singletons["heroine_service"]

    def get_npc_service(self) -> Any:
        """Get NPCService singleton."""
        if "npc_service" not in self._singletons:
            from services.npc_service import NPCService

            self._singletons["npc_service"] = NPCService()
        return self._singletons["npc_service"]

    def get_scene_service(self) -> Any:
        """Get SceneService singleton."""
        if "scene_service" not in self._singletons:
            from services.scene_service import SceneService

            self._singletons["scene_service"] = SceneService()
        return self._singletons["scene_service"]

    def get_simulation_service(self) -> Any:
        """Get SimulationService singleton."""
        if "simulation_service" not in self._singletons:
            from services.simulation_service import SimulationService

            self._singletons["simulation_service"] = SimulationService()
        return self._singletons["simulation_service"]


_container: Container | None = None


def get_container() -> Container:
    """Get the global container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container
