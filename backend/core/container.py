"""
Dependency Injection Container for Pixel Heart OS.

Manages singleton lifetimes and dependency resolution.
"""
from typing import Optional, Type, TypeVar, Dict, Any
from .cache import Cache
from config import Settings


T = TypeVar('T')


class Container:
    """
    Simple dependency injection container.
    Manages service lifetimes and dependencies.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self._cache = Cache(default_ttl=settings.cache_ttl_beads if hasattr(settings, 'cache_ttl_beads') else 60)
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[Type, Any] = {}

    def get_cache(self) -> Cache:
        """Get cache instance (singleton)."""
        if 'cache' not in self._singletons:
            self._singletons['cache'] = self._cache
        return self._cache

    def get_bead_engine(self):
        """Get or create BeadEngine singleton."""
        from beads.engine import BeadEngine

        if 'bead_engine' not in self._singletons:
            self._singletons['bead_engine'] = BeadEngine()
        return self._singletons['bead_engine']

    def get_llm_service(self):
        """Get or create LLMService singleton."""
        from llm.service import LLMService

        if 'llm_service' not in self._singletons:
            self._singletons['llm_service'] = LLMService()
        return self._singletons['llm_service']

    def get_chroma_client(self):
        """Get or create ChromaClient singleton."""
        from vector_store.chroma_client import ChromaClient

        if 'chroma_client' not in self._singletons:
            self._singletons['chroma_client'] = ChromaClient(
                persist_directory=self.settings.chroma_db_path
            )
        return self._singletons['chroma_client']

    def get_bead_repository(self):
        """Get or create BeadRepository."""
        if 'bead_repository' not in self._singletons:
            from infrastructure.database.repositories.bead_repo import BeadRepository
            self._singletons['bead_repository'] = BeadRepository()
        return self._singletons['bead_repository']

    def get_character_repository(self):
        """Get or create CharacterRepository."""
        if 'character_repository' not in self._singletons:
            from infrastructure.database.repositories.character_repo import CharacterRepository
            self._singletons['character_repository'] = CharacterRepository()
        return self._singletons['character_repository']

    def get_relationship_repository(self):
        """Get or create RelationshipRepository."""
        if 'relationship_repository' not in self._singletons:
            from infrastructure.database.repositories.relationship_repo import RelationshipRepository
            self._singletons['relationship_repository'] = RelationshipRepository()
        return self._singletons['relationship_repository']

    def get_bead_service(self):
        """Get or create BeadService."""
        if 'bead_service' not in self._singletons:
            from services.bead_service import BeadService
            self._singletons['bead_service'] = BeadService(
                bead_engine=self.get_bead_engine(),
                bead_repo=self.get_bead_repository(),
                cache=self.get_cache()
            )
        return self._singletons['bead_service']

    def get_heroine_service(self):
        """Get or create HeroineService."""
        if 'heroine_service' not in self._singletons:
            from services.heroine_service import HeroineService
            self._singletons['heroine_service'] = HeroineService(
                llm_service=self.get_llm_service(),
                character_repo=self.get_character_repository(),
                storage=self.get_storage_service()
            )
        return self._singletons['heroine_service']

    def get_npc_service(self):
        """Get or create NPCService."""
        if 'npc_service' not in self._singletons:
            from services.npc_service import NPCService
            self._singletons['npc_service'] = NPCService(
                llm_service=self.get_llm_service(),
                character_repo=self.get_character_repository(),
                chroma_client=self.get_chroma_client()
            )
        return self._singletons['npc_service']

    def get_scene_service(self):
        """Get or create SceneService."""
        if 'scene_service' not in self._singletons:
            from services.scene_service import SceneService
            self._singletons['scene_service'] = SceneService(
                llm_service=self.get_llm_service(),
                chroma_client=self.get_chroma_client()
            )
        return self._singletons['scene_service']

    def get_storage_service(self) -> 'StorageService':
        """Get or create StorageService."""
        if 'storage_service' not in self._singletons:
            from services.storage_service import StorageService
            self._singletons['storage_service'] = StorageService(
                data_dir=self.settings.data_dir
            )
        return self._singletons['storage_service']

    def get_simulation_service(self):
        """Get or create SimulationService."""
        if 'simulation_service' not in self._singletons:
            from services.simulation_service import SimulationService
            self._singletons['simulation_service'] = SimulationService(
                llm_service=self.get_llm_service(),
                bead_service=self.get_bead_service(),
                relationship_repo=self.get_relationship_repository(),
                character_repo=self.get_character_repository()
            )
        return self._singletons['simulation_service']


# Global container instance (will be initialized in main.py)
_container: Optional[Container] = None


def init_container(settings: Settings) -> Container:
    """Initialize global container."""
    global _container
    _container = Container(settings)
    return _container


def get_container() -> Container:
    """Get global container instance."""
    if _container is None:
        raise RuntimeError("Container not initialized. Call init_container() first.")
    return _container
