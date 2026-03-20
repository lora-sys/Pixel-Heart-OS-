"""
Simulation API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from core.container import get_container

router = APIRouter(prefix="/simulation", tags=["simulation"])


class RunTurnRequest(BaseModel):
    player_action: str


@router.post("/run", response_model=Dict[str, Any])
async def run_turn(request: RunTurnRequest):
    """Run a simulation turn."""
    try:
        container = get_container()
        heroine_service = container.get_heroine_service()
        npc_service = container.get_npc_service()
        simulation_service = container.get_simulation_service()

        heroine = await heroine_service.get_heroine()
        if not heroine:
            raise HTTPException(status_code=400, detail="No heroine exists")
        npcs = await npc_service.get_npcs()
        if not npcs:
            raise HTTPException(status_code=400, detail="No NPCs exist")
        result = await simulation_service.run_turn(heroine, npcs, request.player_action)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset", response_model=Dict[str, str])
async def reset_simulation():
    """Reset simulation state."""
    try:
        container = get_container()
        simulation_service = container.get_simulation_service()
        return await simulation_service.reset()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[Dict[str, Any]])
async def get_history():
    """Get conversation history."""
    try:
        container = get_container()
        simulation_service = container.get_simulation_service()
        return await simulation_service.get_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset", response_model=Dict[str, str])
async def reset_simulation():
    """Reset simulation state."""
    try:
        from services.simulation_service import SimulationService

        simulation_service = SimulationService()
        return await simulation_service.reset()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", response_model=List[Dict[str, Any]])
async def get_history():
    """Get conversation history."""
    try:
        from services.simulation_service import SimulationService

        simulation_service = SimulationService()
        return await simulation_service.get_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
