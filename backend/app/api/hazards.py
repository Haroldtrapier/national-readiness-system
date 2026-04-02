from fastapi import APIRouter

router = APIRouter()

@router.get("/national-summary")
async def get_national_hazards():
    return {"hazards": [], "timestamp": "2026-04-01T23:21:37Z"}

@router.post("/refresh")
async def refresh_hazards():
    return {"message": "Hazard data refreshed", "count": 0}
