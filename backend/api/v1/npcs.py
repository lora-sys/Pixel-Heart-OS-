"""
NPCs API endpoints.
Thin layer: validates input, calls service, returns response.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..schemas import NPCResponse, NPCRefineRequest, NPCRefineResponse
from interfaces.api.deps import get_npc_service
from services.npc_service import NPCService

router = APIRouter()


@router.post("/generate", response_model=List[NPCResponse])
async def generate_npcs(
    npc_service: NPCService = Depends(get_npc_service)
):
    """
    Generate Protector, Competitor, Shadow NPCs based on heroine's soul.
    """
    try:
        npcs = await npc_service.generate_npcs(
            roles=["protector", "competitor", "shadow"]
        )
        return [NPCResponse(**npc) for npc in npcs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate NPCs: {str(e)}")


@router.get("", response_model=List[NPCResponse])
async def list_npcs(
    npc_service: NPCService = Depends(get_npc_service)
):
    """List all NPCs."""
    npcs = await npc_service.list_npcs()
    return [NPCResponse(**npc) for npc in npcs]


@router.get("/{npc_id}", response_model=NPCResponse)
async def get_npc(
    npc_id: str,
    npc_service: NPCService = Depends(get_npc_service)
):
    """Get NPC by ID."""
    npc = await npc_service.get_npc(npc_id)
    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")
    return NPCResponse(**npc)


@router.patch("/{npc_id}/refine", response_model=NPCRefineResponse)
async def refine_npc(
    npc_id: str,
    request: NPCRefineRequest,
    npc_service: NPCService = Depends(get_npc_service)
):
    """
    AI collaborative editing: refine an NPC based on user feedback.
    Returns original and suggested versions for review.
    """
    try:
        result = await npc_service.refine_npc(npc_id, request.feedback)
        original = {
            "soul": result["soul"],
            "identity": result["identity"],
            "voice": result["voice"]
        }
        diff = []  # TODO: compute diff between original and refined
        return NPCRefineResponse(
            original=original,
            suggested=result,
            diff=diff
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refinement failed: {str(e)}")


@router.post("/{npc_id}/refine/apply")
async def apply_refinement(
    npc_id: str,
    refined_data: dict,
    npc_service: NPCService = Depends(get_npc_service)
):
    """
    Apply the refined changes (after user approval).
    """
    try:
        # In our architecture, refine_npc already applies changes
        # This endpoint could be a no-op or we could re-apply if needed
        # For now, return success
        return {"status": "applied", "npc_id": npc_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to apply refinement: {str(e)}")
