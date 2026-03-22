from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.hazards import CountyHazardImpact, ReadinessAssessment, HazardEvent, HazardType
from app.models.geography import County, State, FemaRegion
from app.utils.scoring import hazard_score, readiness_band, confidence_band


def score_county(county_id: str, db: Session) -> dict | None:
    impacts = (
        db.query(CountyHazardImpact)
        .filter(CountyHazardImpact.county_id == county_id)
        .all()
    )
    if not impacts:
        return None

    max_impact = max(impacts, key=lambda x: x.hazard_score or 0)
    return {
        "county_id": county_id,
        "hazard_score": max_impact.hazard_score,
        "readiness_band": max_impact.readiness_band,
        "confidence_band": max_impact.confidence_band,
    }


def get_national_summary(db: Session) -> dict:
    active_events = db.query(HazardEvent).filter(HazardEvent.event_status == "active").count()

    risk_counties = (
        db.query(CountyHazardImpact)
        .filter(CountyHazardImpact.readiness_band.in_(["ORANGE", "RED", "BLACK"]))
        .distinct(CountyHazardImpact.county_id)
        .count()
    )

    top_impacts = (
        db.query(
            CountyHazardImpact,
            County,
            HazardEvent,
            HazardType,
            State,
        )
        .join(County, CountyHazardImpact.county_id == County.id)
        .join(HazardEvent, CountyHazardImpact.hazard_event_id == HazardEvent.id)
        .join(HazardType, HazardEvent.hazard_type_id == HazardType.id)
        .join(State, County.state_id == State.id)
        .order_by(CountyHazardImpact.hazard_score.desc())
        .limit(10)
        .all()
    )

    top_hazards = []
    for impact, county, event, htype, state in top_impacts:
        top_hazards.append({
            "hazard_code": htype.hazard_code,
            "hazard_name": htype.hazard_name,
            "state_code": state.state_code,
            "county_name": county.county_name,
            "county_fips": county.county_fips,
            "probability_score": impact.probability_score,
            "severity_score": impact.severity_score,
            "confidence_score": event.confidence_score,
            "readiness_band": impact.readiness_band,
            "confidence_band": impact.confidence_band,
        })

    return {
        "active_hazards": active_events,
        "counties_at_risk": risk_counties,
        "top_hazards": top_hazards,
    }


def get_region_summary(region_number: int, db: Session) -> dict:
    region = db.query(FemaRegion).filter(FemaRegion.region_number == region_number).first()
    if not region:
        return {"error": "Region not found"}

    states = db.query(State).filter(State.fema_region_id == region.id).all()
    state_ids = [s.id for s in states]

    counties = db.query(County).filter(County.state_id.in_(state_ids)).all()
    county_ids = [c.id for c in counties]

    impacts = (
        db.query(
            CountyHazardImpact,
            County,
            HazardEvent,
            HazardType,
            State,
        )
        .join(County, CountyHazardImpact.county_id == County.id)
        .join(HazardEvent, CountyHazardImpact.hazard_event_id == HazardEvent.id)
        .join(HazardType, HazardEvent.hazard_type_id == HazardType.id)
        .join(State, County.state_id == State.id)
        .filter(CountyHazardImpact.county_id.in_(county_ids))
        .order_by(CountyHazardImpact.hazard_score.desc())
        .limit(20)
        .all()
    )

    hazards = []
    max_score = 0.0
    risk_count = 0
    for impact, county, event, htype, state in impacts:
        if (impact.hazard_score or 0) > max_score:
            max_score = impact.hazard_score or 0
        if impact.readiness_band in ("ORANGE", "RED", "BLACK"):
            risk_count += 1
        hazards.append({
            "hazard_code": htype.hazard_code,
            "hazard_name": htype.hazard_name,
            "state_code": state.state_code,
            "county_name": county.county_name,
            "county_fips": county.county_fips,
            "probability_score": impact.probability_score,
            "severity_score": impact.severity_score,
            "confidence_score": event.confidence_score,
            "readiness_band": impact.readiness_band,
            "confidence_band": impact.confidence_band,
        })

    return {
        "region_number": region.region_number,
        "region_name": region.region_name,
        "active_hazards": len(hazards),
        "counties_at_risk": risk_count,
        "readiness_band": readiness_band(max_score),
        "hazards": hazards,
    }
