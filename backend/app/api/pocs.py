from fastapi import APIRouter

router = APIRouter()

@router.get("/fema/{region_id}")
async def get_fema_pocs(region_id: str):
    return {"region_id": region_id, "pocs": []}

@router.get("/sema/{state_code}")
async def get_state_pocs(state_code: str):
    return {"state_code": state_code, "pocs": []}

@router.get("/local/{county_fips}")
async def get_local_pocs(county_fips: str):
    return {"county_fips": county_fips, "pocs": []}
