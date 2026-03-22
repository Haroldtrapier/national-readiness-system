from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.geography import FemaRegion, State, County

router = APIRouter(prefix="/geography", tags=["Geography"])


@router.get("/regions")
def list_regions(db: Session = Depends(get_db)):
    regions = db.query(FemaRegion).order_by(FemaRegion.region_number).all()
    return [
        {
            "id": r.id,
            "region_number": r.region_number,
            "region_name": r.region_name,
            "headquarters_city": r.headquarters_city,
            "headquarters_state": r.headquarters_state,
        }
        for r in regions
    ]


@router.get("/states")
def list_states(region_number: int | None = None, db: Session = Depends(get_db)):
    query = db.query(State).order_by(State.state_code)
    if region_number:
        region = db.query(FemaRegion).filter(FemaRegion.region_number == region_number).first()
        if region:
            query = query.filter(State.fema_region_id == region.id)
    states = query.all()
    return [
        {
            "id": s.id,
            "state_code": s.state_code,
            "state_name": s.state_name,
            "fema_region_id": s.fema_region_id,
            "is_territory": s.is_territory,
        }
        for s in states
    ]


@router.get("/counties")
def list_counties(state_code: str | None = None, db: Session = Depends(get_db)):
    query = db.query(County)
    if state_code:
        state = db.query(State).filter(State.state_code == state_code.upper()).first()
        if state:
            query = query.filter(County.state_id == state.id)
    counties = query.order_by(County.county_name).all()
    return [
        {
            "id": c.id,
            "county_name": c.county_name,
            "county_fips": c.county_fips,
            "population": c.population,
            "is_coastal": c.is_coastal,
            "latitude": c.latitude,
            "longitude": c.longitude,
        }
        for c in counties
    ]
