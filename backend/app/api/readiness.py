from fastapi import APIRouter
from app.services.readiness_service import ReadinessService

router = APIRouter()

@router.get("/national")
async def get_national_readiness():
    return {"scope": "national", "data": ReadinessService.get_national_summary(None)}

@router.get("/regions/{region_id}")
async def get_region_readiness(region_id: str):
    return {"scope": "region", "data": ReadinessService.get_region_readiness(None, region_id)}
