"""
Beads API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from typing import List, Optional
from datetime import datetime

from database import get_session, Bead, ActionType, EmotionTag
from ..schemas import (
    BeadCreate, BeadResponse, BeadSummary,
    BranchCreate, BranchResponse,
    BeadDiffResponse
)

router = APIRouter()


@router.get("/timeline", response_model=List[BeadSummary])
async def get_timeline(
    branch: str = Query("main", description="Branch name"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    """
    Retrieve the narrative timeline (beads) for a given branch.
    Ordered by timestamp ascending (from root to HEAD).
    """
    stmt = (
        select(Bead)
        .where(Bead.branch_name == branch)
        .order_by(Bead.timestamp.asc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    beads = result.scalars().all()
    return beads


@router.post("", response_model=BeadResponse)
async def create_bead(
    bead_data: BeadCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new Bead and update branch HEAD.
    """
    # TODO: Implement hash calculation, DAG validation
    # For now: basic insert
    from hashlib import sha1
    import json

    content_str = json.dumps(bead_data.content, sort_keys=True)
    parent_str = bead_data.parent_id or ""
    hash_input = (parent_str + content_str + bead_data.action.value).encode('utf-8')
    bead_id = sha1(hash_input).hexdigest()

    # Check if parent exists (if provided)
    if bead_data.parent_id:
        parent_stmt = select(Bead).where(Bead.id == bead_data.parent_id)
        parent_result = await session.execute(parent_stmt)
        parent = parent_result.scalar_one_or_none()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent bead not found")

    new_bead = Bead(
        id=bead_id,
        parent_id=bead_data.parent_id,
        branch_name=bead_data.branch_name,
        action=bead_data.action,
        emotion_tag=bead_data.emotion_tag,
        content=bead_data.content,
        signature=bead_data.signature
    )

    session.add(new_bead)
    await session.flush()

    # Update HEAD for this branch (simple version: just store in a separate table or cache)
    # For now, rely on querying max timestamp per branch

    await session.commit()
    await session.refresh(new_bead)

    return new_bead


@router.post("/branch", response_model=BranchResponse)
async def create_branch(
    branch_data: BranchCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new branch from a given bead.
    """
    from_bead_id = branch_data.from_bead_id

    # Verify source bead exists
    stmt = select(Bead).where(Bead.id == from_bead_id)
    result = await session.execute(stmt)
    from_bead = result.scalar_one_or_none()
    if not from_bead:
        raise HTTPException(status_code=404, detail="Source bead not found")

    # Check if branch already exists
    existing = select(Bead).where(
        Bead.branch_name == branch_data.branch_name,
        Bead.id == from_bead_id
    )
    existing_result = await session.execute(existing)
    if existing_result.first():
        raise HTTPException(status_code=400, detail="Branch already exists with this name")

    # Create a new Bead that marks branch creation
    branch_bead_id = f"branch_{branch_data.branch_name}_{datetime.utcnow().timestamp()}"
    # In real implementation, calculate proper hash

    # For now: just return success (actual branching is implicit via branch_name)
    return BranchResponse(
        branch_name=branch_data.branch_name,
        head_bead_id=from_bead_id,
        message=f"Branch '{branch_data.branch_name}' created from bead {from_bead_id[:8]}"
    )


@router.get("/diff/{bead_id1}/{bead_id2}", response_model=BeadDiffResponse)
async def diff_beads(
    bead_id1: str,
    bead_id2: str,
    session: AsyncSession = Depends(get_session)
):
    """
    Compute diff between two beads (typically parent-child).
    """
    stmt1 = select(Bead).where(Bead.id == bead_id1)
    stmt2 = select(Bead).where(Bead.id == bead_id2)
    result1 = await session.execute(stmt1)
    result2 = await session.execute(stmt2)
    bead1 = result1.scalar_one_or_none()
    bead2 = result2.scalar_one_or_none()

    if not bead1 or not bead2:
        raise HTTPException(status_code=404, detail="One or both beads not found")

    # Simple diff: compare content JSON
    # In production, use proper diff algorithm
    changes = []
    for key in set(bead2.content.keys()) | set(bead1.content.keys()):
        val1 = bead1.content.get(key)
        val2 = bead2.content.get(key)
        if val1 != val2:
            changes.append({
                "field": key,
                "from": val1,
                "to": val2
            })

    return BeadDiffResponse(
        bead_id_earlier=bead_id1 if bead1.timestamp < bead2.timestamp else bead_id2,
        bead_id_later=bead_id2 if bead2.timestamp > bead1.timestamp else bead_id1,
        changes=changes
    )


@router.get("/branches")
async def list_branches(session: AsyncSession = Depends(get_session)):
    """
    List all branches and their HEAD bead.
    """
    from sqlalchemy import func

    # Get latest bead per branch (assuming max timestamp)
    stmt = (
        select(
            Bead.branch_name,
            func.max(Bead.timestamp).label("max_ts")
        )
        .group_by(Bead.branch_name)
        .order_by(Bead.branch_name)
    )
    result = await session.execute(stmt)
    branches = result.all()

    # For each branch, get the bead with that timestamp
    branches_data = []
    for branch_name, max_ts in branches:
        bead_stmt = select(Bead).where(
            Bead.branch_name == branch_name,
            Bead.timestamp == max_ts
        )
        bead_result = await session.execute(bead_stmt)
        head_bead = bead_result.scalar_one_or_none()
        if head_bead:
            branches_data.append({
                "name": branch_name,
                "head_bead_id": head_bead.id,
                "head_timestamp": head_bead.timestamp
            })

    return {"branches": branches_data}
