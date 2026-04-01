from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.services.readiness_scoring_service import get_region_summary, get_national_summary
from app.services.supply_planning_service import get_supply_recommendations
from app.services.vendor_matching_service import get_all_vendors
from app.models.contacts import Poc
from app.models.geography import FemaRegion, State
from app.models.organizations import Organization

ACTION_TEMPLATES = {
    "HURRICANE": [
        "Pre-stage water, MREs, tarps, cots at designated staging areas",
        "Pre-negotiate fuel and generator support contracts",
        "Activate logistics ESF coordination",
        "Prepare shelter surge contracts",
        "Pre-position IMT, comms support, and debris planning teams",
        "Alert healthcare coalitions and dialysis networks",
        "Validate evacuation route / contraflow plans",
        "Coordinate with National Guard for transportation support",
    ],
    "FLOOD": [
        "Stage sandbags and pumps at key river crossings",
        "Pre-position swift-water rescue teams",
        "Activate flood-zone shelters",
        "Coordinate road closure communications",
        "Deploy water purification units to staging areas",
    ],
    "TORNADO": [
        "Alert search and rescue teams",
        "Stage chainsaws and debris clearance equipment",
        "Prepare temporary shelter locations",
        "Pre-position medical triage resources",
        "Coordinate power restoration with utilities",
    ],
    "SEVERE_CONVECTIVE": [
        "Monitor SPC outlooks for escalation",
        "Pre-position power restoration crews",
        "Stage debris clearance equipment",
    ],
    "WINTER_STORM": [
        "Open warming shelters",
        "Pre-stage fuel, blankets, and heating units",
        "Coordinate road treatment with DOT",
        "Prepare medical transport for vulnerable populations",
        "Stage generator support for critical facilities",
    ],
    "HEAT": [
        "Open cooling centers",
        "Stage water distribution points",
        "Coordinate EMS surge for heat-related emergencies",
        "Initiate wellness checks for vulnerable populations",
    ],
    "EARTHQUAKE": [
        "Activate Urban Search and Rescue teams",
        "Deploy damage assessment teams",
        "Initiate comms restoration",
        "Prioritize hospital and bridge inspection",
        "Stage medical surge resources",
    ],
    "WILDFIRE": [
        "Open air quality shelters",
        "Coordinate evacuation management",
        "Stage water supply support",
        "Deploy damage assessment teams",
    ],
}


def generate_region_brief(region_number: int, db: Session) -> dict:
    summary = get_region_summary(region_number, db)
    if "error" in summary:
        return summary

    region = db.query(FemaRegion).filter(FemaRegion.region_number == region_number).first()

    pocs = (
        db.query(Poc, Organization)
        .outerjoin(Organization, Poc.organization_id == Organization.id)
        .filter(Poc.fema_region_id == region.id)
        .filter(Poc.is_active == True)
        .all()
    )

    poc_list = [
        {
            "name": p.contact_name,
            "role": p.title or p.contact_type,
            "phone": p.phone,
            "email": p.email,
            "availability": p.availability_type,
        }
        for p, org in pocs
    ]

    hazard_codes = set()
    for h in summary.get("hazards", []):
        hazard_codes.add(h.get("hazard_code", ""))

    supply_needs = []
    actions = []
    for code in hazard_codes:
        recs = get_supply_recommendations(code, summary["readiness_band"])
        supply_needs.extend(
            {
                "item_name": r["item_name"],
                "required": r["quantity"],
                "available": 0,
                "shortage": r["quantity"],
                "shortage_pct": 100.0,
            }
            for r in recs
        )
        actions.extend(ACTION_TEMPLATES.get(code, []))

    threats = [
        {
            "hazard_type": h.get("hazard_name", ""),
            "area": f"{h.get('county_name', '')} County, {h.get('state_code', '')}",
            "risk_level": h.get("readiness_band", "GREEN"),
            "confidence": h.get("confidence_band", "LOW"),
            "narrative": f"{h.get('hazard_name', '')} risk in {h.get('county_name', '')} County",
        }
        for h in summary.get("hazards", [])[:5]
    ]

    vendors = get_all_vendors(db)[:5]
    vendor_briefs = [
        {
            "vendor_name": v["organization_name"],
            "capability": v["vendor_type"],
            "sla_hours": v.get("response_sla_hours"),
            "contract_ready": v.get("contract_ready", False),
        }
        for v in vendors
    ]

    return {
        "title": f"Region {region_number} Operational Brief",
        "scope": f"FEMA Region {region_number}",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "readiness_band": summary["readiness_band"],
        "threats": threats,
        "supply_needs": supply_needs,
        "recommended_vendors": vendor_briefs,
        "key_contacts": poc_list,
        "recommended_actions": list(set(actions)),
    }


def generate_national_brief(db: Session) -> dict:
    summary = get_national_summary(db)

    hazard_codes = set()
    for h in summary.get("top_hazards", []):
        hazard_codes.add(h.get("hazard_code", ""))

    actions = []
    for code in hazard_codes:
        actions.extend(ACTION_TEMPLATES.get(code, []))

    threats = [
        {
            "hazard_type": h.get("hazard_name", ""),
            "area": f"{h.get('county_name', '')} County, {h.get('state_code', '')}",
            "risk_level": h.get("readiness_band", "GREEN"),
            "confidence": h.get("confidence_band", "LOW"),
            "narrative": f"{h.get('hazard_name', '')} risk detected",
        }
        for h in summary.get("top_hazards", [])[:10]
    ]

    max_band = "GREEN"
    for h in summary.get("top_hazards", []):
        band = h.get("readiness_band", "GREEN")
        if band in ("BLACK", "RED", "ORANGE", "YELLOW"):
            max_band = band
            break

    return {
        "title": "National Operational Brief",
        "scope": "National",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "readiness_band": max_band,
        "threats": threats,
        "supply_needs": [],
        "recommended_vendors": [],
        "key_contacts": [],
        "recommended_actions": list(set(actions)),
    }
