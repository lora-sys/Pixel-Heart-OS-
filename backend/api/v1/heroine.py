"""
Heroine API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from database import get_session, Character
from ..schemas import HeroineCreateRequest, HeroineResponse, SoulStructure, Identity, VoiceConfig
from storage.file_system import save_heroine_data
from llm.service import LLMService

router = APIRouter()


@router.post("/create", response_model=HeroineResponse)
async def create_heroine(
    request: HeroineCreateRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new heroine from user description.
    - Parses description with LLM to extract soul structure
    - Generates identity and voice config
    - Saves to file storage
    - Creates initial Bead
    """
    try:
        llm = LLMService()

        # Parse soul from description
        soul_data = await llm.parse_heroine(request.description)

        # Generate identity (for now: simple defaults)
        # In full implementation, LLM would generate proper identity
        identity_data = Identity(
            name="Heroine",  # TODO: LLM generate name
            age=20,
            appearance="Generated from soul structure",
            personality="See soul traits",
            backstory="To be written"
        )

        # Generate voice config
        voice_data = VoiceConfig(
            speech_patterns={"type": "conversational"},
            vocabulary={"level": "neutral"},
            emotional_tone={"primary": "warm"}
        )

        # Save to file system
        heroine_id = await save_heroine_data(soul_data, identity_data, voice_data)

        # Create Character record
        heroine = Character(
            id=heroine_id,
            name=identity_data.name,
            role="heroine",
            soul_file_path=f"data/heroine/{heroine_id}/soul.md",
            identity_file_path=f"data/heroine/{heroine_id}/identity.md",
            voice_file_path=f"data/heroine/{heroine_id}/voice.toml",
            cached_soul=soul_data.dict(),
            cached_identity=identity_data.dict(),
            cached_voice=voice_data.dict()
        )
        session.add(heroine)
        await session.commit()

        return HeroineResponse(
            id=heroine_id,
            soul=soul_data,
            identity=identity_data,
            voice=voice_data,
            created_at=heroine.created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create heroine: {str(e)}")


@router.get("/", response_model=Optional[HeroineResponse])
async def get_heroine(
    session: AsyncSession = Depends(get_session)
):
    """
    Get current heroine (if created).
    """
    stmt = select(Character).where(Character.role == "heroine").limit(1)
    result = await session.execute(stmt)
    heroine = result.scalar_one_or_none()

    if not heroine:
        return None

    return HeroineResponse(
        id=heroine.id,
        soul=SoulStructure(**heroine.cached_soul),
        identity=Identity(**heroine.cached_identity),
        voice=VoiceConfig(**heroine.cached_voice),
        created_at=heroine.created_at
    )
