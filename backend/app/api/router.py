from fastapi import APIRouter
from app.api.v1 import hazards, readiness, supplies, vendors, pocs, agencies, it_assets, briefs, geography

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(geography.router)
api_router.include_router(hazards.router)
api_router.include_router(readiness.router)
api_router.include_router(supplies.router)
api_router.include_router(vendors.router)
api_router.include_router(pocs.router)
api_router.include_router(agencies.router)
api_router.include_router(it_assets.router)
api_router.include_router(briefs.router)
