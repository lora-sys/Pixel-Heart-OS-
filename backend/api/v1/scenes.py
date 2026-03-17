"""
Scene API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from services.scene_service import SceneService
from services.heroine_service import HeroineService
from services.npc_service import NPCService

router = APIRouter(prefix="/scenes", tags=["scenes"])
scene_service = SceneService()
heroine_service = HeroineService()
npc_service = NPCService()


class GenerateSceneRequest(BaseModel):
    location: str = ""


@router.post("/", response_model=Dict[str, Any])
async def generate_scene(request: GenerateSceneRequest):
    """Generate a scene."""
    heroine = await heroine_service.get_heroine()
    if not heroine:
        raise HTTPException(status_code=400, detail="No heroine exists")
    npcs = await npc_service.get_npcs()
    result = await scene_service.generate_scene(heroine, npcs, request.location)
    return result


@router.get("/", response_model=List[Dict[str, Any]])
async def get_scenes():
    """Get all scenes."""
    return await scene_service.get_scenes()
