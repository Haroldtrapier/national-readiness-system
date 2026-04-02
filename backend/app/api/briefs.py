from fastapi import APIRouter

router = APIRouter()

@router.get("/national")
async def get_national_brief():
    return {"scope": "national", "brief": "Operational Brief Ready"}

@router.get("/region/{region_id}")
async def get_region_brief(region_id: str):
    return {"scope": "region", "brief": "Region Brief Ready"}
