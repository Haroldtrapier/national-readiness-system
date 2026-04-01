from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.database import engine
from app.models.base import Base
from app.api.router import api_router

import app.models.geography  # noqa
import app.models.hazards  # noqa
import app.models.supplies  # noqa
import app.models.organizations  # noqa
import app.models.vendors  # noqa
import app.models.contacts  # noqa
import app.models.agencies  # noqa
import app.models.it_assets  # noqa

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="National Hazard Readiness & FEMA/SEMA Preparation System with IT Equipment Tracking",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {
        "system": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "modules": [
            "Disaster Readiness Command",
            "Government IT Equipment Demand Command",
        ],
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
