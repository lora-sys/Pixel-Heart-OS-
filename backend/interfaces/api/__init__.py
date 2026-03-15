"""
API interfaces package.
"""
from .deps import get_container, get_bead_service, get_heroine_service, get_npc_service, get_scene_service, get_simulation_service

__all__ = [
    "get_container",
    "get_bead_service",
    "get_heroine_service",
    "get_npc_service",
    "get_scene_service",
    "get_simulation_service"
]
