from sqlalchemy.orm import Session
from app.models.supplies import SupplyPackage, SupplyPackageItem, SupplyItem, SupplyRequirement
from app.models.hazards import ReadinessAssessment, CountyHazardImpact, HazardEvent, HazardType
from app.models.geography import County
from app.utils.scoring import shortage_score

HAZARD_SUPPLY_RULES: dict[str, dict[str, list[tuple[str, int]]]] = {
    "HURRICANE": {
        "ORANGE": [
            ("Bottled Water", 10000),
            ("Meals Ready to Eat", 5000),
            ("Blue Tarp", 1000),
            ("Portable Generator", 100),
            ("Diesel Fuel (gallons)", 5000),
            ("Cot", 500),
            ("Emergency Blanket", 1000),
        ],
        "RED": [
            ("Bottled Water", 50000),
            ("Meals Ready to Eat", 25000),
            ("Blue Tarp", 5000),
            ("Portable Generator", 500),
            ("Diesel Fuel (gallons)", 25000),
            ("Cot", 2500),
            ("Emergency Blanket", 5000),
            ("Rescue Boat", 20),
        ],
        "BLACK": [
            ("Bottled Water", 200000),
            ("Meals Ready to Eat", 100000),
            ("Blue Tarp", 20000),
            ("Portable Generator", 2000),
            ("Diesel Fuel (gallons)", 100000),
            ("Cot", 10000),
            ("Emergency Blanket", 20000),
            ("Rescue Boat", 50),
        ],
    },
    "FLOOD": {
        "ORANGE": [
            ("Water Pump", 25),
            ("Sandbag", 25000),
            ("Rescue Boat", 5),
            ("PPE Kit", 200),
            ("Water Purification Unit", 5),
        ],
        "RED": [
            ("Water Pump", 50),
            ("Sandbag", 50000),
            ("Rescue Boat", 15),
            ("PPE Kit", 500),
            ("Water Purification Unit", 10),
            ("Bottled Water", 20000),
        ],
    },
    "TORNADO": {
        "ORANGE": [
            ("Chainsaw", 50),
            ("PPE Kit", 200),
            ("Emergency Blanket", 500),
            ("Cot", 200),
            ("First Aid Kit", 100),
        ],
        "RED": [
            ("Chainsaw", 200),
            ("PPE Kit", 1000),
            ("Emergency Blanket", 2000),
            ("Cot", 1000),
            ("First Aid Kit", 500),
            ("Portable Generator", 100),
        ],
    },
    "SEVERE_CONVECTIVE": {
        "ORANGE": [
            ("Chainsaw", 30),
            ("PPE Kit", 100),
            ("Emergency Blanket", 200),
            ("Portable Generator", 50),
        ],
    },
    "WINTER_STORM": {
        "ORANGE": [
            ("Emergency Blanket", 2500),
            ("Portable Heater", 200),
            ("Diesel Fuel (gallons)", 10000),
            ("Portable Generator", 100),
        ],
        "RED": [
            ("Emergency Blanket", 5000),
            ("Portable Heater", 500),
            ("Diesel Fuel (gallons)", 25000),
            ("Portable Generator", 250),
            ("Cot", 1000),
        ],
    },
    "HEAT": {
        "ORANGE": [
            ("Bottled Water", 25000),
            ("Portable AC Unit", 100),
            ("First Aid Kit", 200),
        ],
        "RED": [
            ("Bottled Water", 100000),
            ("Portable AC Unit", 500),
            ("First Aid Kit", 500),
        ],
    },
    "EARTHQUAKE": {
        "RED": [
            ("PPE Kit", 1000),
            ("First Aid Kit", 1000),
            ("Portable Generator", 500),
            ("Bottled Water", 50000),
            ("Meals Ready to Eat", 25000),
            ("Cot", 2000),
        ],
    },
    "WILDFIRE": {
        "ORANGE": [
            ("Bottled Water", 10000),
            ("PPE Kit", 500),
            ("First Aid Kit", 200),
        ],
    },
}


def get_supply_recommendations(hazard_code: str, severity_band: str) -> list[dict]:
    rules = HAZARD_SUPPLY_RULES.get(hazard_code, {})
    items = rules.get(severity_band, [])
    return [{"item_name": name, "quantity": qty} for name, qty in items]


def get_county_supply_requirements(county_fips: str, db: Session) -> list[dict]:
    county = db.query(County).filter(County.county_fips == county_fips).first()
    if not county:
        return []

    impacts = (
        db.query(CountyHazardImpact, HazardEvent, HazardType)
        .join(HazardEvent, CountyHazardImpact.hazard_event_id == HazardEvent.id)
        .join(HazardType, HazardEvent.hazard_type_id == HazardType.id)
        .filter(CountyHazardImpact.county_id == county.id)
        .filter(CountyHazardImpact.readiness_band.in_(["ORANGE", "RED", "BLACK"]))
        .all()
    )

    all_requirements: dict[str, dict] = {}
    for impact, event, htype in impacts:
        recs = get_supply_recommendations(htype.hazard_code, impact.readiness_band)
        for rec in recs:
            name = rec["item_name"]
            if name in all_requirements:
                all_requirements[name]["required_quantity"] = max(
                    all_requirements[name]["required_quantity"], rec["quantity"]
                )
            else:
                all_requirements[name] = {
                    "item_name": name,
                    "required_quantity": rec["quantity"],
                    "available_quantity": 0,
                    "shortage_quantity": rec["quantity"],
                    "shortage_pct": 100.0,
                    "priority_level": impact.readiness_band,
                }

    return list(all_requirements.values())
