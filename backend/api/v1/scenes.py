"""
Scene API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from core.container import get_container

router = APIRouter(prefix="/scenes", tags=["scenes"])


class GenerateSceneRequest(BaseModel):
    location: str = ""


@router.post("/", response_model=Dict[str, Any])
async def generate_scene(request: GenerateSceneRequest):
    """Generate a scene."""
    try:
        container = get_container()
        heroine_service = container.get_heroine_service()
        npc_service = container.get_npc_service()
        scene_service = container.get_scene_service()

        heroine = await heroine_service.get_heroine()
        if not heroine:
            raise HTTPException(status_code=400, detail="No heroine exists")
        npcs = await npc_service.get_npcs()
        result = await scene_service.generate_scene(heroine, npcs, request.location)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Dict[str, Any]])
async def get_scenes():
    """Get all scenes."""
    try:
        container = get_container()
        scene_service = container.get_scene_service()
        return await scene_service.get_scenes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[Dict[str, Any]])
async def get_scenes():
    """Get all scenes."""
    try:
        from services.scene_service import SceneService

        scene_service = SceneService()
        return await scene_service.get_scenes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
