"""
NPC API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from core.container import get_container

router = APIRouter(prefix="/npcs", tags=["npcs"])


class GenerateNPCsRequest(BaseModel):
    heroine_description: Optional[str] = None
    count: int = 3


class UpdateNPCRequest(BaseModel):
    relationship: Optional[float] = None
    name: Optional[str] = None


@router.post("/", response_model=List[Dict[str, Any]])
async def generate_npcs(request: GenerateNPCsRequest):
    """Generate NPCs for the heroine."""
    try:
        container = get_container()
        heroine_service = container.get_heroine_service()
        npc_service = container.get_npc_service()

        heroine_data = await heroine_service.get_heroine()
        if not heroine_data:
            heroine_data = {"identity": {"name": "Unknown"}}
        result = await npc_service.generate_npcs(heroine_data, request.count)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Dict[str, Any]])
async def get_npcs():
    """Get all NPCs."""
    try:
        container = get_container()
        npc_service = container.get_npc_service()
        return await npc_service.get_npcs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{npc_id}", response_model=Optional[Dict[str, Any]])
async def update_npc(npc_id: str, request: UpdateNPCRequest):
    """Update an NPC."""
    try:
        container = get_container()
        npc_service = container.get_npc_service()

        updates = request.model_dump(exclude_none=True)
        result = await npc_service.update_npc(npc_id, updates)
        if result is None:
            raise HTTPException(status_code=404, detail="NPC not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Dict[str, Any]])
async def get_npcs():
    """Get all NPCs."""
    try:
        from services.npc_service import NPCService

        npc_service = NPCService()
        return await npc_service.get_npcs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{npc_id}", response_model=Optional[Dict[str, Any]])
async def update_npc(npc_id: str, request: UpdateNPCRequest):
    """Update an NPC."""
    try:
        from services.npc_service import NPCService

        npc_service = NPCService()

        updates = request.model_dump(exclude_none=True)
        result = await npc_service.update_npc(npc_id, updates)
        if result is None:
            raise HTTPException(status_code=404, detail="NPC not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
