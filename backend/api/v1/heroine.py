"""
Heroine API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from services.heroine_service import HeroineService

router = APIRouter(prefix="/heroine", tags=["heroine"])
heroine_service = HeroineService()


class CreateHeroineRequest(BaseModel):
    description: str


@router.post("/", response_model=Dict[str, Any])
async def create_heroine(request: CreateHeroineRequest):
    """Create a heroine from description."""
    try:
        result = await heroine_service.create_heroine(request.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=Optional[Dict[str, Any]])
async def get_heroine():
    """Get current heroine."""
    result = await heroine_service.get_heroine()
    if result is None:
        raise HTTPException(status_code=404, detail="No heroine found")
    return result
