"""
Simulation API endpoints - Using service layer.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from ..schemas import (
    SimulationTurnRequest, SimulationTurnResponse,
    SimulationStateResponse, NPCResponse
)
from interfaces.api.deps import get_simulation_service, get_bead_service
from services.simulation_service import SimulationService
from services.bead_service import BeadService

router = APIRouter()


@router.get("/state", response_model=SimulationStateResponse)
async def get_simulation_state(
    simulation_service: SimulationService = Depends(get_simulation_service),
    bead_service: BeadService = Depends(get_bead_service)
):
    """Get current simulation state."""
    try:
        state = await simulation_service.get_simulation_state()

        return SimulationStateResponse(**state)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/turn", response_model=SimulationTurnResponse)
async def take_turn(
    request: SimulationTurnRequest,
    simulation_service: SimulationService = Depends(get_simulation_service)
):
    """
    Process a player action and generate NPC responses.
    Core simulation loop.
    """
    try:
        result = await simulation_service.process_turn(
            player_action=request.player_action,
            current_bead_id=request.current_bead_id,
            branch_name=request.branch_name or "main"
        )

        return SimulationTurnResponse(**result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")
