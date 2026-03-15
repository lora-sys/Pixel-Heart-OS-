"""
API v1 router - aggregates all endpoints.
"""
from fastapi import APIRouter

from . import beads, heroine, npcs, scenes, simulation

router = APIRouter()

# Include all sub-routers
router.include_router(beads.router, prefix="/beads", tags=["beads"])
router.include_router(heroine.router, prefix="/heroine", tags=["heroine"])
router.include_router(npcs.router, prefix="/npcs", tags=["npcs"])
router.include_router(scenes.router, prefix="/scenes", tags=["scenes"])
router.include_router(simulation.router, prefix="/simulate", tags=["simulation"])

__all__ = ["router"]
