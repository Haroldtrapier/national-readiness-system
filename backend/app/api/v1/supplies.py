from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.supplies import SupplyCategory, SupplyItem
from app.services.supply_planning_service import get_supply_recommendations, get_county_supply_requirements

router = APIRouter(prefix="/supplies", tags=["Supplies"])


@router.get("/catalog")
def supply_catalog(db: Session = Depends(get_db)):
    categories = db.query(SupplyCategory).all()
    items = db.query(SupplyItem).filter(SupplyItem.is_active == True).all()

    return {
        "categories": [
            {"id": c.id, "category_code": c.category_code, "category_name": c.category_name}
            for c in categories
        ],
        "items": [
            {"id": i.id, "item_name": i.item_name, "unit_of_measure": i.unit_of_measure}
            for i in items
        ],
    }


@router.get("/packages/{hazard_code}")
def supply_packages(hazard_code: str, severity_band: str = "ORANGE"):
    recs = get_supply_recommendations(hazard_code.upper(), severity_band.upper())
    return {
        "hazard_code": hazard_code.upper(),
        "severity_band": severity_band.upper(),
        "items": recs,
    }


@router.get("/requirements/{county_fips}")
def county_requirements(county_fips: str, db: Session = Depends(get_db)):
    reqs = get_county_supply_requirements(county_fips, db)
    return {
        "county_fips": county_fips,
        "requirements": reqs,
    }
