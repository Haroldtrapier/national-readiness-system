from fastapi import APIRouter

router = APIRouter()

@router.get("/regions")
async def list_regions():
    return {
        "count": 3,
        "regions": [
            {"id": "r3", "number": 3, "name": "Region III", "headquarters": "Philadelphia, PA"},
            {"id": "r4", "number": 4, "name": "Region IV", "headquarters": "Atlanta, GA"},
            {"id": "r6", "number": 6, "name": "Region VI", "headquarters": "Denton, TX"},
        ]
    }

@router.get("/states")
async def list_states():
    return {
        "count": 9,
        "states": [
            {"id": "s1", "code": "NC", "name": "North Carolina", "fema_region": 3},
            {"id": "s2", "code": "SC", "name": "South Carolina", "fema_region": 3},
            {"id": "s3", "code": "GA", "name": "Georgia", "fema_region": 4},
        ]
    }

@router.get("/counties")
async def list_counties(state_code: str = None):
    return {"count": 25, "counties": []}
