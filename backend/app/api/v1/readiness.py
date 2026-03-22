from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.readiness_scoring_service import get_national_summary, get_region_summary, score_county
from app.models.geography import County

router = APIRouter(prefix="/readiness", tags=["Readiness"])


@router.get("/national")
def national_readiness(db: Session = Depends(get_db)):
    return get_national_summary(db)


@router.get("/regions/{region_number}")
def region_readiness(region_number: int, db: Session = Depends(get_db)):
    return get_region_summary(region_number, db)


@router.get("/states/{state_code}")
def state_readiness(state_code: str, db: Session = Depends(get_db)):
    from app.models.geography import State
    state = db.query(State).filter(State.state_code == state_code.upper()).first()
    if not state:
        return {"error": "State not found"}

    counties = db.query(County).filter(County.state_id == state.id).all()
    results = []
    for county in counties:
        score = score_county(county.id, db)
        if score:
            score["county_name"] = county.county_name
            score["county_fips"] = county.county_fips
            results.append(score)

    results.sort(key=lambda x: x.get("hazard_score", 0), reverse=True)
    return {
        "state_code": state.state_code,
        "state_name": state.state_name,
        "counties": results,
    }


@router.get("/counties/{county_fips}")
def county_readiness(county_fips: str, db: Session = Depends(get_db)):
    county = db.query(County).filter(County.county_fips == county_fips).first()
    if not county:
        return {"error": "County not found"}

    result = score_county(county.id, db)
    if not result:
        return {"county_fips": county_fips, "readiness_band": "GREEN", "hazard_score": 0}

    result["county_name"] = county.county_name
    return result
