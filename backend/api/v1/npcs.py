"""
NPC API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from services.npc_service import NPCService
from services.heroine_service import HeroineService

router = APIRouter(prefix="/npcs", tags=["npcs"])
npc_service = NPCService()
heroine_service = HeroineService()


class GenerateNPCsRequest(BaseModel):
    heroine_description: Optional[str] = None
    count: int = 3


class UpdateNPCRequest(BaseModel):
    relationship: Optional[float] = None
    name: Optional[str] = None


@router.post("/", response_model=List[Dict[str, Any]])
async def generate_npcs(request: GenerateNPCsRequest):
    """Generate NPCs for the heroine."""
    heroine_data = await heroine_service.get_heroine()
    if not heroine_data:
        heroine_data = {"identity": {"name": "Unknown"}}
    result = await npc_service.generate_npcs(heroine_data, request.count)
    return result


@router.get("/", response_model=List[Dict[str, Any]])
async def get_npcs():
    """Get all NPCs."""
    return await npc_service.get_npcs()


@router.patch("/{npc_id}", response_model=Optional[Dict[str, Any]])
async def update_npc(npc_id: str, request: UpdateNPCRequest):
    """Update an NPC."""
    updates = request.model_dump(exclude_none=True)
    result = await npc_service.update_npc(npc_id, updates)
    if result is None:
        raise HTTPException(status_code=404, detail="NPC not found")
    return result
