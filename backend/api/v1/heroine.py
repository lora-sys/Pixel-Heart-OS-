"""
Heroine API endpoints.
Thin layer: validates input, calls service, returns response.
"""
from fastapi import APIRouter, Depends, HTTPException

from ..schemas import HeroineCreateRequest, HeroineResponse
from interfaces.api.deps import get_heroine_service
from services.heroine_service import HeroineService

router = APIRouter()


@router.post("/create", response_model=HeroineResponse)
async def create_heroine(
    request: HeroineCreateRequest,
    heroine_service: HeroineService = Depends(get_heroine_service)
):
    """
    Create a new heroine from user description.
    - Parses description with LLM to extract soul structure
    - Generates identity and voice config
    - Saves to file storage
    - Creates database record
    """
    try:
        heroine = await heroine_service.create_heroine(
            description=request.description,
            input_mode=request.input_mode
        )

        return HeroineResponse(**heroine)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create heroine: {str(e)}")


@router.get("/", response_model=HeroineResponse)
async def get_heroine(
    heroine_service: HeroineService = Depends(get_heroine_service)
):
    """
    Get current heroine (if created).
    Returns the most recently created heroine.
    """
    # For now, get first heroine (there should only be one)
    # Future: store current heroine ID in app state or use query param
    heroine = await heroine_service.get_heroine()  # Get first heroine

    if not heroine:
        raise HTTPException(status_code=404, detail="No heroine found")

    return HeroineResponse(**heroine)
