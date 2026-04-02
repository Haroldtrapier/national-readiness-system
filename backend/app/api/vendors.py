from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_vendors():
    return {"count": 0, "vendors": []}
