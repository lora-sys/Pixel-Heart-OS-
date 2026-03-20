"""
Heroine API endpoints.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from core.container import get_container

router = APIRouter(prefix="/heroine", tags=["heroine"])


class CreateHeroineRequest(BaseModel):
    description: str


@router.post("/", response_model=Dict[str, Any])
async def create_heroine(request: CreateHeroineRequest):
    """Create a heroine from description."""
    try:
        container = get_container()
        heroine_service = container.get_heroine_service()
        result = await heroine_service.create_heroine(request.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=Optional[Dict[str, Any]])
async def get_heroine():
    """Get current heroine."""
    try:
        container = get_container()
        heroine_service = container.get_heroine_service()
        result = await heroine_service.get_heroine()
        if result is None:
            raise HTTPException(status_code=404, detail="No heroine found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=Optional[Dict[str, Any]])
async def get_heroine():
    """Get current heroine."""
    try:
        container = get_container()
        llm = container.get_llm_service()
        storage = container.get_storage_service()

        from services.heroine_service import HeroineService
        from services.bead_service import BeadService

        bead_service = BeadService()
        heroine_service = HeroineService(
            llm_service=llm, storage_service=storage, bead_service=bead_service
        )

        result = await heroine_service.get_heroine()
        if result is None:
            raise HTTPException(status_code=404, detail="No heroine found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
