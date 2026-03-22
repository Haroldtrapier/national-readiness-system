import httpx
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.hazards import HazardEvent, HazardType, CountyHazardImpact
from app.models.geography import State, County
from app.utils.scoring import hazard_score, readiness_band, confidence_band
from app.core.config import get_settings

settings = get_settings()

HAZARD_CODE_MAP = {
    "Tornado Warning": "TORNADO",
    "Tornado Watch": "TORNADO",
    "Severe Thunderstorm Warning": "SEVERE_CONVECTIVE",
    "Severe Thunderstorm Watch": "SEVERE_CONVECTIVE",
    "Flash Flood Warning": "FLOOD",
    "Flood Warning": "FLOOD",
    "Flood Watch": "FLOOD",
    "Coastal Flood Warning": "FLOOD",
    "Hurricane Warning": "HURRICANE",
    "Hurricane Watch": "HURRICANE",
    "Tropical Storm Warning": "HURRICANE",
    "Tropical Storm Watch": "HURRICANE",
    "Winter Storm Warning": "WINTER_STORM",
    "Winter Storm Watch": "WINTER_STORM",
    "Blizzard Warning": "WINTER_STORM",
    "Ice Storm Warning": "WINTER_STORM",
    "Excessive Heat Warning": "HEAT",
    "Heat Advisory": "HEAT",
    "Extreme Cold Warning": "WINTER_STORM",
    "Wind Chill Warning": "WINTER_STORM",
    "Earthquake Warning": "EARTHQUAKE",
    "Fire Weather Watch": "WILDFIRE",
    "Red Flag Warning": "WILDFIRE",
}

SEVERITY_MAP = {
    "Extreme": 1.0,
    "Severe": 0.8,
    "Moderate": 0.6,
    "Minor": 0.4,
    "Unknown": 0.3,
}

CERTAINTY_MAP = {
    "Observed": 1.0,
    "Likely": 0.8,
    "Possible": 0.5,
    "Unlikely": 0.2,
    "Unknown": 0.3,
}

URGENCY_MAP = {
    "Immediate": 1.0,
    "Expected": 0.8,
    "Future": 0.5,
    "Past": 0.2,
    "Unknown": 0.3,
}


async def fetch_nws_alerts() -> list[dict]:
    headers = {"User-Agent": settings.NWS_USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{settings.NWS_API_BASE}/alerts/active", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data.get("features", [])


async def fetch_usgs_earthquakes() -> list[dict]:
    params = {
        "format": "geojson",
        "starttime": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "minmagnitude": 3.0,
        "orderby": "time",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{settings.USGS_EARTHQUAKE_API}/query", params=params)
        resp.raise_for_status()
        data = resp.json()
        return data.get("features", [])


def process_nws_alert(alert: dict, db: Session) -> HazardEvent | None:
    props = alert.get("properties", {})
    event_name = props.get("event", "")
    hazard_code = HAZARD_CODE_MAP.get(event_name)
    if not hazard_code:
        return None

    hazard_type = db.query(HazardType).filter(HazardType.hazard_code == hazard_code).first()
    if not hazard_type:
        return None

    ext_id = props.get("id", "")
    existing = db.query(HazardEvent).filter(HazardEvent.external_event_id == ext_id).first()
    if existing:
        return existing

    severity_val = SEVERITY_MAP.get(props.get("severity", "Unknown"), 0.3)
    certainty_val = CERTAINTY_MAP.get(props.get("certainty", "Unknown"), 0.3)
    urgency_val = URGENCY_MAP.get(props.get("urgency", "Unknown"), 0.3)

    prob = round((certainty_val * 0.6 + urgency_val * 0.4), 2)

    event = HazardEvent(
        hazard_type_id=hazard_type.id,
        event_source="NWS",
        external_event_id=ext_id,
        event_name=f"{event_name}: {props.get('headline', '')}",
        event_status="active" if props.get("status") == "Actual" else "test",
        probability_score=prob,
        severity_score=severity_val,
        confidence_score=certainty_val,
        issued_at=props.get("sent"),
        start_at=props.get("effective"),
        end_at=props.get("expires"),
        source_payload=props,
    )
    db.add(event)
    db.flush()

    fips_codes = props.get("geocode", {}).get("SAME", [])
    for fips in fips_codes:
        county_fips = fips[1:] if fips.startswith("0") and len(fips) == 6 else fips
        county = db.query(County).filter(County.county_fips == county_fips).first()
        if not county:
            continue

        exposure = 0.5
        if county.population and county.population > 500000:
            exposure = 0.9
        elif county.population and county.population > 100000:
            exposure = 0.7

        vulnerability = 0.6 if county.is_coastal else 0.4

        score = hazard_score(prob, severity_val, exposure, vulnerability, certainty_val)

        impact = CountyHazardImpact(
            county_id=county.id,
            hazard_event_id=event.id,
            probability_score=prob,
            severity_score=severity_val,
            exposure_score=exposure,
            vulnerability_score=vulnerability,
            hazard_score=score,
            readiness_band=readiness_band(score),
            confidence_band=confidence_band(certainty_val),
        )
        db.add(impact)

    return event


def process_earthquake(eq: dict, db: Session) -> HazardEvent | None:
    props = eq.get("properties", {})
    geometry = eq.get("geometry", {})
    coords = geometry.get("coordinates", [])

    hazard_type = db.query(HazardType).filter(HazardType.hazard_code == "EARTHQUAKE").first()
    if not hazard_type:
        return None

    ext_id = eq.get("id", "")
    existing = db.query(HazardEvent).filter(HazardEvent.external_event_id == ext_id).first()
    if existing:
        return existing

    mag = props.get("mag", 0)
    severity = min(mag / 9.0, 1.0) if mag else 0.3

    event = HazardEvent(
        hazard_type_id=hazard_type.id,
        event_source="USGS",
        external_event_id=ext_id,
        event_name=props.get("title", "Earthquake"),
        event_status="active",
        probability_score=1.0,
        severity_score=round(severity, 2),
        confidence_score=0.95,
        source_payload=props,
    )
    db.add(event)
    db.flush()
    return event


async def ingest_all(db: Session) -> dict:
    stats = {"nws_alerts": 0, "earthquakes": 0, "errors": []}

    try:
        alerts = await fetch_nws_alerts()
        for alert in alerts:
            result = process_nws_alert(alert, db)
            if result:
                stats["nws_alerts"] += 1
    except Exception as e:
        stats["errors"].append(f"NWS: {str(e)}")

    try:
        quakes = await fetch_usgs_earthquakes()
        for eq in quakes:
            result = process_earthquake(eq, db)
            if result:
                stats["earthquakes"] += 1
    except Exception as e:
        stats["errors"].append(f"USGS: {str(e)}")

    db.commit()
    return stats
