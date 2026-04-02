from fastapi import APIRouter

router = APIRouter()

@router.get("/agencies/{agency_id}")
async def get_agency_it(agency_id: str):
    return {"agency_id": agency_id, "assets": []}

@router.get("/forecast/states/{state_code}")
async def get_state_it_forecast(state_code: str):
    return {"state_code": state_code, "forecast": []}
