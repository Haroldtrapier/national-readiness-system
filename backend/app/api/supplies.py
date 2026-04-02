from fastapi import APIRouter

router = APIRouter()

@router.get("/catalog")
async def get_supply_catalog():
    return {"categories": []}

@router.get("/packages/{hazard_code}")
async def get_supply_packages(hazard_code: str):
    return {"package": None}
