"""
Beads API endpoints.
Thin layer: validates input, calls service, returns response.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from ..schemas import (
    BeadCreate, BeadResponse, BeadSummary,
    BranchCreate, BranchResponse,
    BeadDiffResponse
)
from interfaces.api.deps import get_bead_service
from services.bead_service import BeadService

router = APIRouter()


@router.get("/timeline", response_model=List[BeadSummary])
async def get_timeline(
    branch: str = Query("main", description="Branch name"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    bead_service: BeadService = Depends(get_bead_service)
):
    """
    Retrieve the narrative timeline (beads) for a given branch.
    Ordered by timestamp ascending (from root to HEAD).
    """
    beads = await bead_service.get_timeline(
        branch_name=branch,
        limit=limit,
        offset=offset
    )
    return beads


@router.post("", response_model=BeadResponse)
async def create_bead(
    bead_data: BeadCreate,
    bead_service: BeadService = Depends(get_bead_service)
):
    """
    Create a new Bead using BeadService.
    Ensures consistent ID hashing and DAG validation.
    """
    bead = await bead_service.create_bead(
        action=bead_data.action,
        content=bead_data.content,
        parent_id=bead_data.parent_id,
        branch_name=bead_data.branch_name,
        emotion_tag=bead_data.emotion_tag,
        signature=bead_data.signature
    )

    return BeadResponse(**bead)


@router.post("/branch", response_model=BranchResponse)
async def create_branch(
    branch_data: BranchCreate,
    bead_service: BeadService = Depends(get_bead_service)
):
    """
    Create a new branch from a given bead.
    """
    result = await bead_service.create_branch(
        branch_name=branch_data.branch_name,
        from_bead_id=branch_data.from_bead_id
    )

    return BranchResponse(**result)


@router.get("/diff/{bead_id1}/{bead_id2}", response_model=BeadDiffResponse)
async def diff_beads(
    bead_id1: str,
    bead_id2: str,
    bead_service: BeadService = Depends(get_bead_service)
):
    """
    Compute diff between two beads (typically parent-child).
    """
    diff = await bead_service.diff_beads(bead_id1, bead_id2)

    return BeadDiffResponse(**diff)


@router.get("/branches")
async def list_branches(
    bead_service: BeadService = Depends(get_bead_service)
):
    """
    List all branches and their HEAD bead.
    """
    branches = await bead_service.list_branches()
    return {"branches": branches}
