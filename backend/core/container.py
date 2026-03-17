"""
Container for dependency injection.
"""

from typing import Dict, Any
from backend.llm.service import LLMService
from backend.beads.engine import BeadEngine
from backend.storage.file_system import FileSystemService


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


_container: Container = None


def get_container() -> Container:
    """Get the global container instance."""
    global _container
    if _container is None:
        _container = Container()
    return _container
