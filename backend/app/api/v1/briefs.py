from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.brief_generation_service import generate_region_brief, generate_national_brief

router = APIRouter(prefix="/briefs", tags=["Operational Briefs"])


@router.get("/national")
def national_brief(db: Session = Depends(get_db)):
    return generate_national_brief(db)


@router.get("/region/{region_number}")
def region_brief(region_number: int, db: Session = Depends(get_db)):
    return generate_region_brief(region_number, db)
