"""
FastAPI Dependency Injection providers.
"""
from typing import Annotated
from fastapi import Depends

from core.container import Container, get_container
from services.bead_service import BeadService
from services.heroine_service import HeroineService
from services.npc_service import NPCService
from services.scene_service import SceneService
from services.simulation_service import SimulationService
from services.storage_service import StorageService


def get_bead_service(
    container: Annotated[Container, Depends(get_container)]
) -> BeadService:
    """Get BeadService with dependencies."""
    return container.get_bead_service()


def get_heroine_service(
    container: Annotated[Container, Depends(get_container)]
) -> HeroineService:
    """Get HeroineService with dependencies."""
    return container.get_heroine_service()


def get_npc_service(
    container: Annotated[Container, Depends(get_container)]
) -> NPCService:
    """Get NPCService with dependencies."""
    return container.get_npc_service()


def get_scene_service(
    container: Annotated[Container, Depends(get_container)]
) -> SceneService:
    """Get SceneService with dependencies."""
    return container.get_scene_service()


def get_simulation_service(
    container: Annotated[Container, Depends(get_container)]
) -> SimulationService:
    """Get SimulationService with dependencies."""
    return container.get_simulation_service()


