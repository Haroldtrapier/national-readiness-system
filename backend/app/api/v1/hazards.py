from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.core.database import get_db
from app.services.readiness_scoring_service import get_national_summary, get_region_summary
from app.services.hazard_ingestion_service import ingest_all
from app.models.hazards import HazardEvent, HazardType, CountyHazardImpact
from app.models.geography import County, State

router = APIRouter(prefix="/hazards", tags=["Hazards"])


@router.get("/national-summary")
def national_summary(db: Session = Depends(get_db)):
    summary = get_national_summary(db)
    summary["timestamp"] = datetime.now(timezone.utc).isoformat()
    return summary


@router.get("/regions/{region_number}")
def region_hazards(region_number: int, db: Session = Depends(get_db)):
    return get_region_summary(region_number, db)


@router.get("/states/{state_code}")
def state_hazards(state_code: str, db: Session = Depends(get_db)):
    state = db.query(State).filter(State.state_code == state_code.upper()).first()
    if not state:
        return {"error": "State not found"}

    counties = db.query(County).filter(County.state_id == state.id).all()
    county_ids = [c.id for c in counties]

    impacts = (
        db.query(CountyHazardImpact, County, HazardEvent, HazardType)
        .join(County, CountyHazardImpact.county_id == County.id)
        .join(HazardEvent, CountyHazardImpact.hazard_event_id == HazardEvent.id)
        .join(HazardType, HazardEvent.hazard_type_id == HazardType.id)
        .filter(CountyHazardImpact.county_id.in_(county_ids))
        .order_by(CountyHazardImpact.hazard_score.desc())
        .all()
    )

    hazards = []
    for impact, county, event, htype in impacts:
        hazards.append({
            "hazard_code": htype.hazard_code,
            "hazard_name": htype.hazard_name,
            "county_name": county.county_name,
            "county_fips": county.county_fips,
            "probability_score": impact.probability_score,
            "severity_score": impact.severity_score,
            "readiness_band": impact.readiness_band,
            "confidence_band": impact.confidence_band,
        })

    return {
        "state_code": state.state_code,
        "state_name": state.state_name,
        "hazards": hazards,
    }


@router.get("/counties/{county_fips}")
def county_hazards(county_fips: str, db: Session = Depends(get_db)):
    county = db.query(County).filter(County.county_fips == county_fips).first()
    if not county:
        return {"error": "County not found"}

    impacts = (
        db.query(CountyHazardImpact, HazardEvent, HazardType)
        .join(HazardEvent, CountyHazardImpact.hazard_event_id == HazardEvent.id)
        .join(HazardType, HazardEvent.hazard_type_id == HazardType.id)
        .filter(CountyHazardImpact.county_id == county.id)
        .order_by(CountyHazardImpact.hazard_score.desc())
        .all()
    )

    hazards = []
    for impact, event, htype in impacts:
        hazards.append({
            "hazard_code": htype.hazard_code,
            "hazard_name": htype.hazard_name,
            "probability_score": impact.probability_score,
            "severity_score": impact.severity_score,
            "hazard_score": impact.hazard_score,
            "readiness_band": impact.readiness_band,
            "confidence_band": impact.confidence_band,
        })

    return {
        "county_name": county.county_name,
        "county_fips": county.county_fips,
        "hazards": hazards,
    }


@router.post("/refresh")
async def refresh_hazards(db: Session = Depends(get_db)):
    stats = await ingest_all(db)
    return {"status": "complete", "stats": stats}
