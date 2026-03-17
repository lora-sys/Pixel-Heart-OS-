"""
Simulation API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from services.simulation_service import SimulationService
from services.heroine_service import HeroineService
from services.npc_service import NPCService

router = APIRouter(prefix="/simulation", tags=["simulation"])
simulation_service = SimulationService()
heroine_service = HeroineService()
npc_service = NPCService()


class RunTurnRequest(BaseModel):
    player_action: str


@router.post("/run", response_model=Dict[str, Any])
async def run_turn(request: RunTurnRequest):
    """Run a simulation turn."""
    heroine = await heroine_service.get_heroine()
    if not heroine:
        raise HTTPException(status_code=400, detail="No heroine exists")
    npcs = await npc_service.get_npcs()
    if not npcs:
        raise HTTPException(status_code=400, detail="No NPCs exist")
    result = await simulation_service.run_turn(heroine, npcs, request.player_action)
    return result


@router.post("/reset", response_model=Dict[str, str])
async def reset_simulation():
    """Reset simulation state."""
    return await simulation_service.reset()


@router.get("/history", response_model=List[Dict[str, Any]])
async def get_history():
    """Get conversation history."""
    return await simulation_service.get_history()
