"""
Scenes API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database import get_session, Scene
from ..schemas import SceneResponse
from storage.file_system import save_scene_data
from llm.service import LLMService

router = APIRouter()


@router.post("/generate", response_model=List[SceneResponse])
async def generate_scenes(
    session: AsyncSession = Depends(get_session)
):
    """
    Generate scenes based on heroine's preferences.
    """
    try:
        # Get heroine soul to extract preferences
        from database import Character
        stmt = select(Character).where(Character.role == "heroine")
        result = await session.execute(stmt)
        heroine = result.scalar_one_or_none()

        if not heroine:
            raise HTTPException(status_code=400, detail="Create heroine first")

        preferences = heroine.cached_soul.get("scene_preferences", [])

        llm = LLMService()
        scenes = []

        # Generate 3-5 scenes
        for i in range(3):
            scene_data = await llm.generate_scene(preferences)
            scene_id = f"scene_{heroine.id[:8]}_{i}"

            # Save to file system
            await save_scene_data(scene_id, scene_data)

            # Create database record
            scene = Scene(
                id=scene_id,
                name=scene_data["name"],
                description=scene_data["description"],
                config=scene_data,
            )
            session.add(scene)
            await session.flush()

            scenes.append(SceneResponse(
                id=scene.id,
                name=scene.name,
                description=scene.description,
                config=scene.config,
                image_path=scene.image_path,
                created_at=scene.created_at
            ))

        await session.commit()
        return scenes

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate scenes: {str(e)}")


@router.get("", response_model=List[SceneResponse])
async def list_scenes(
    session: AsyncSession = Depends(get_session)
):
    """List all scenes."""
    stmt = select(Scene).order_by(Scene.created_at.desc())
    result = await session.execute(stmt)
    scenes = result.scalars().all()

    return [
        SceneResponse(
            id=s.id,
            name=s.name,
            description=s.description,
            config=s.config,
            image_path=s.image_path,
            created_at=s.created_at
        )
        for s in scenes
    ]


@router.get("/{scene_id}", response_model=SceneResponse)
async def get_scene(
    scene_id: str,
    session: AsyncSession = Depends(get_session)
):
    """Get scene by ID."""
    stmt = select(Scene).where(Scene.id == scene_id)
    result = await session.execute(stmt)
    scene = result.scalar_one_or_none()

    if not scene:
        raise HTTPException(status_code=404, detail="Scene not found")

    return SceneResponse(
        id=scene.id,
        name=scene.name,
        description=scene.description,
        config=scene.config,
        image_path=scene.image_path,
        created_at=scene.created_at
    )
