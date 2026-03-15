"""
Scenes API endpoints.
Thin layer: validates input, calls service, returns response.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from ..schemas import SceneResponse
from interfaces.api.deps import get_scene_service, get_heroine_service
from services.scene_service import SceneService

router = APIRouter()


@router.post("/generate", response_model=List[SceneResponse])
async def generate_scenes(
    scene_service: SceneService = Depends(get_scene_service),
    heroine_service: HeroineService = Depends(get_heroine_service)
):
    """
    Generate scenes based on heroine's preferences.
    """
    try:
        # Get current heroine (simplified - get first)
        # TODO: proper heroine retrieval
        heroine = await heroine_service.get_heroine("heroine")
        if not heroine:
            raise HTTPException(status_code=400, detail="Create heroine first")

        preferences = heroine["soul"].get("scene_preferences", [])

        scenes = await scene_service.generate_scenes(
            heroine_preferences=preferences,
            count=3
        )

        return [SceneResponse(**scene) for scene in scenes]

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate scenes: {str(e)}")


@router.get("", response_model=List[SceneResponse])
async def list_scenes(
    scene_service: SceneService = Depends(get_scene_service)
):
    """List all scenes."""
    # Scene service currently only offers generation and search
    # For listing, we'd need a SceneRepository
    # For now, return empty list (future: add scene repository)
    return []


@router.get("/{scene_id}", response_model=SceneResponse)
async def get_scene(
    scene_id: str,
    scene_service: SceneService = Depends(get_scene_service)
):
    """Get scene by ID."""
    # Scene service currently doesn't have get by ID
    # This would be from database via SceneRepository
    raise HTTPException(status_code=501, detail="Not implemented yet")
