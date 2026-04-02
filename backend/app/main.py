from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import create_tables
from app.api import geography, readiness, hazards, supplies, vendors, pocs, it_assets, briefs

app = FastAPI(
    title="National Readiness System API",
    description="AI-powered disaster readiness and supply intelligence platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    create_tables()

app.include_router(geography.router, prefix="/api/v1/geography", tags=["Geography"])
app.include_router(hazards.router, prefix="/api/v1/hazards", tags=["Hazards"])
app.include_router(readiness.router, prefix="/api/v1/readiness", tags=["Readiness"])
app.include_router(supplies.router, prefix="/api/v1/supplies", tags=["Supplies"])
app.include_router(vendors.router, prefix="/api/v1/vendors", tags=["Vendors"])
app.include_router(pocs.router, prefix="/api/v1/pocs", tags=["POCs"])
app.include_router(it_assets.router, prefix="/api/v1/it-assets", tags=["IT Assets"])
app.include_router(briefs.router, prefix="/api/v1/briefs", tags=["Briefs"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "national-readiness-system"}

@app.get("/")
async def root():
    return {"message": "National Readiness System", "docs": "/docs", "version": "1.0.0"}
