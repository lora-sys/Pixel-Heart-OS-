"""
Beads API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from services.bead_service import BeadService

router = APIRouter(prefix="/beads", tags=["beads"])
bead_service = BeadService()


class CreateBeadRequest(BaseModel):
    parent_id: Optional[str] = None
    content: Dict[str, Any]
    action: str
    branch_name: str = "main"
    emotion_tag: Optional[str] = None


@router.post("/", response_model=Dict[str, Any])
async def create_bead(request: CreateBeadRequest):
    """Create a new bead."""
    bead_id = await bead_service.create_bead(
        request.parent_id,
        request.content,
        request.action,
        request.branch_name,
        request.emotion_tag,
    )
    bead = await bead_service.get_bead(bead_id)
    return bead


@router.get("/", response_model=List[Dict[str, Any]])
async def get_beads(branch: str = "main", limit: int = 50):
    """Get beads for a branch."""
    return await bead_service.get_timeline(branch, limit)


@router.get("/{bead_id}", response_model=Optional[Dict[str, Any]])
async def get_bead(bead_id: str):
    """Get a specific bead."""
    bead = await bead_service.get_bead(bead_id)
    if bead is None:
        raise HTTPException(status_code=404, detail="Bead not found")
    return bead


@router.post("/branch", response_model=Dict[str, str])
async def create_branch(branch_name: str, from_bead_id: str):
    """Create a new branch."""
    result = await bead_service.create_branch(branch_name, from_bead_id)
    return {"branch_id": result}
