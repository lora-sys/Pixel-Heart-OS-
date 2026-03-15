"""
NPCs API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database import get_session, Character
from ..schemas import NPCResponse, NPCRefineRequest, NPCRefineResponse
from storage.file_system import save_npc_data, load_npc_data
from llm.service import LLMService

router = APIRouter()


@router.post("/generate", response_model=List[NPCResponse])
async def generate_npcs(
    session: AsyncSession = Depends(get_session)
):
    """
    Generate Protector, Competitor, Shadow NPCs based on heroine's soul.
    """
    try:
        # Get heroine
        stmt = select(Character).where(Character.role == "heroine")
        result = await session.execute(stmt)
        heroine = result.scalar_one_or_none()

        if not heroine:
            raise HTTPException(status_code=400, detail="Create heroine first")

        llm = LLMService()
        npcs = []

        for role in ["protector", "competitor", "shadow"]:
            npc_data = await llm.generate_npc(heroine.cached_soul, role)

            # Generate unique ID
            npc_id = f"npc_{role}_{heroine.id[:8]}"

            # Save to file system
            await save_npc_data(npc_id, npc_data)

            # Create Character record
            npc = Character(
                id=npc_id,
                name=npc_data["identity"]["name"],
                role=role,
                soul_file_path=f"data/npcs/{npc_id}/soul.md",
                identity_file_path=f"data/npcs/{npc_id}/identity.md",
                voice_file_path=f"data/npcs/{npc_id}/voice.toml",
                cached_soul=npc_data["soul"],
                cached_identity=npc_data["identity"],
                cached_voice=npc_data["voice"]
            )
            session.add(npc)
            await session.flush()

            npcs.append(NPCResponse(
                id=npc.id,
                name=npc.name,
                role=npc.role,
                relationship_to_heroine=role,
                soul=npc.cached_soul,
                identity=npc.cached_identity,
                voice=npc.cached_voice,
                created_at=npc.created_at
            ))

        await session.commit()
        return npcs

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate NPCs: {str(e)}")


@router.get("", response_model=List[NPCResponse])
async def list_npcs(
    session: AsyncSession = Depends(get_session)
):
    """List all NPCs."""
    stmt = select(Character).where(Character.role.in_(["protector", "competitor", "shadow"]))
    result = await session.execute(stmt)
    npcs = result.scalars().all()

    return [
        NPCResponse(
            id=npc.id,
            name=npc.name,
            role=npc.role,
            relationship_to_heroine=npc.role,
            soul=npc.cached_soul,
            identity=npc.cached_identity,
            voice=npc.cached_voice,
            created_at=npc.created_at
        )
        for npc in npcs
    ]


@router.get("/{npc_id}", response_model=NPCResponse)
async def get_npc(
    npc_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get NPC by ID."""
    stmt = select(Character).where(Character.id == npc_id)
    result = await session.execute(stmt)
    npc = result.scalar_one_or_none()

    if not npc:
        raise HTTPException(status_code=404, detail="NPC not found")

    return NPCResponse(
        id=npc.id,
        name=npc.name,
        role=npc.role,
        relationship_to_heroine=npc.role,
        soul=npc.cached_soul,
        identity=npc.cached_identity,
        voice=npc.cached_voice,
        created_at=npc.created_at
    )


@router.patch("/{npc_id}/refine", response_model=NPCRefineResponse)
async def refine_npc(
    npc_id: str,
    request: NPCRefineRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    AI collaborative editing: refine an NPC based on user feedback.
    Returns original and suggested versions for review.
    """
    try:
        # Get current NPC data
        npc_data = await load_npc_data(npc_id)
        if not npc_data:
            raise HTTPException(status_code=404, detail="NPC data not found")

        llm = LLMService()
        refined = await llm.refine_npc(npc_data, request.feedback)

        # Compute diff
        diff = []
        for key in set(refined.keys()) | set(npc_data.keys()):
            old_val = npc_data.get(key)
            new_val = refined.get(key)
            if old_val != new_val:
                diff.append({
                    "field": key,
                    "from": old_val,
                    "to": new_val
                })

        return NPCRefineResponse(
            original=npc_data,
            suggested=refined,
            diff=diff
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refinement failed: {str(e)}")


@router.post("/{npc_id}/refine/apply")
async def apply_refinement(
    npc_id: str,
    refined_data: dict,
    session: AsyncSession = Depends(get_session)
):
    """
    Apply the refined changes (after user approval).
    """
    try:
        # Save new data
        await save_npc_data(npc_id, refined_data)

        # Update database cache
        stmt = select(Character).where(Character.id == npc_id)
        result = await session.execute(stmt)
        npc = result.scalar_one_or_none()

        if npc:
            npc.cached_soul = refined_data.get("soul", npc.cached_soul)
            npc.cached_identity = refined_data.get("identity", npc.cached_identity)
            npc.cached_voice = refined_data.get("voice", npc.cached_voice)
            await session.commit()

        return {"status": "applied", "npc_id": npc_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to apply refinement: {str(e)}")
