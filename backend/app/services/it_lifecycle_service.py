from datetime import date
from sqlalchemy.orm import Session
from app.models.it_assets import ItAsset, ItDemandForecast, ItItemCategory
from app.models.agencies import Agency, AgencySite
from app.models.organizations import Organization
from app.utils.scoring import it_replacement_score, surge_device_quantity


def get_agency_it_summary(agency_id: str, db: Session) -> dict:
    agency = (
        db.query(Agency, Organization)
        .join(Organization, Agency.organization_id == Organization.id)
        .filter(Agency.id == agency_id)
        .first()
    )
    if not agency:
        return {"error": "Agency not found"}

    ag, org = agency
    assets = db.query(ItAsset).filter(ItAsset.agency_id == agency_id).all()

    today = date.today()
    total = len(assets)
    expiring_90d = 0
    high_risk = 0

    asset_list = []
    for a in assets:
        score = it_replacement_score(
            purchase_date=a.purchase_date,
            warranty_end_date=a.warranty_end_date,
            security_gap=(a.security_status == "upgrade_needed"),
            critical_role=False,
            lifecycle_years=a.lifecycle_years or 4,
        )

        if a.warranty_end_date:
            days_left = (a.warranty_end_date - today).days
            if 0 < days_left <= 90:
                expiring_90d += 1

        if score >= 70:
            high_risk += 1

        asset_list.append({
            "id": a.id,
            "asset_tag": a.asset_tag,
            "asset_type": a.asset_type,
            "manufacturer": a.manufacturer,
            "model": a.model,
            "serial_number": a.serial_number,
            "operating_system": a.operating_system,
            "purchase_date": a.purchase_date.isoformat() if a.purchase_date else None,
            "warranty_end_date": a.warranty_end_date.isoformat() if a.warranty_end_date else None,
            "assigned_user": a.assigned_user,
            "operating_status": a.operating_status,
            "security_status": a.security_status,
            "replacement_score": score,
        })

    forecasts = (
        db.query(ItDemandForecast, ItItemCategory)
        .join(ItItemCategory, ItDemandForecast.it_item_category_id == ItItemCategory.id)
        .filter(ItDemandForecast.agency_id == agency_id)
        .all()
    )

    forecast_list = []
    surge_total = 0
    for f, cat in forecasts:
        surge_total += f.quantity_needed
        forecast_list.append({
            "id": f.id,
            "item_category": cat.category_name,
            "quantity_needed": f.quantity_needed,
            "date_needed": f.date_needed.isoformat() if f.date_needed else None,
            "reason_code": f.reason_code,
            "confidence_score": f.confidence_score,
            "procurement_action_score": f.procurement_action_score,
            "notes": f.notes,
        })

    return {
        "agency_id": agency_id,
        "agency_name": org.organization_name,
        "total_assets": total,
        "expiring_warranty_90d": expiring_90d,
        "high_risk_replacements": high_risk,
        "surge_devices_needed": surge_total,
        "assets": asset_list,
        "forecasts": forecast_list,
    }


def get_state_it_forecast(state_code: str, db: Session) -> list[dict]:
    from app.models.geography import State

    state = db.query(State).filter(State.state_code == state_code).first()
    if not state:
        return []

    agencies = db.query(Agency).filter(Agency.state_id == state.id).all()
    agency_ids = [a.id for a in agencies]

    forecasts = (
        db.query(ItDemandForecast, ItItemCategory, Agency, Organization)
        .join(ItItemCategory, ItDemandForecast.it_item_category_id == ItItemCategory.id)
        .join(Agency, ItDemandForecast.agency_id == Agency.id)
        .join(Organization, Agency.organization_id == Organization.id)
        .filter(ItDemandForecast.agency_id.in_(agency_ids))
        .all()
    )

    return [
        {
            "agency_name": org.organization_name,
            "item_category": cat.category_name,
            "quantity_needed": f.quantity_needed,
            "date_needed": f.date_needed.isoformat() if f.date_needed else None,
            "reason_code": f.reason_code,
            "confidence_score": f.confidence_score,
            "procurement_action_score": f.procurement_action_score,
        }
        for f, cat, ag, org in forecasts
    ]
