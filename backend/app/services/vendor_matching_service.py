from sqlalchemy.orm import Session
from app.models.vendors import Vendor, VendorSupplyCapability, VendorMatch
from app.models.organizations import Organization
from app.models.supplies import SupplyItem
from app.models.geography import State, FemaRegion
from app.utils.scoring import vendor_fit_score


def find_vendors_for_item(
    item_name: str,
    state_code: str | None,
    db: Session,
) -> list[dict]:
    query = (
        db.query(Vendor, VendorSupplyCapability, Organization)
        .join(Organization, Vendor.organization_id == Organization.id)
        .join(VendorSupplyCapability, VendorSupplyCapability.vendor_id == Vendor.id)
        .filter(Vendor.active_status == True)
    )

    results = query.all()

    matches = []
    for vendor, cap, org in results:
        item_match = 0.8
        geography_fit = 0.5
        capacity_fit = 0.5

        if vendor.contract_ready:
            contract_fit = 1.0
        else:
            contract_fit = 0.3

        speed_fit = 1.0 - min((vendor.lead_time_days or 7) / 14, 1.0) if vendor.lead_time_days else 0.5
        emergency_fit = 1.0 if vendor.emergency_surge_capable else 0.3

        score = vendor_fit_score(
            item_match=item_match,
            geography_fit=geography_fit,
            capacity_fit=capacity_fit,
            contract_fit=contract_fit,
            speed_fit=speed_fit,
            emergency_fit=emergency_fit,
        )

        matches.append({
            "vendor_id": vendor.id,
            "vendor_name": org.organization_name,
            "vendor_type": vendor.vendor_type,
            "fit_score": score,
            "contract_ready": vendor.contract_ready,
            "emergency_surge_capable": vendor.emergency_surge_capable,
            "response_sla_hours": vendor.response_sla_hours,
            "lead_time_days": vendor.lead_time_days,
            "geographic_coverage": vendor.geographic_coverage,
        })

    matches.sort(key=lambda x: x["fit_score"], reverse=True)
    return matches


def get_all_vendors(db: Session) -> list[dict]:
    results = (
        db.query(Vendor, Organization)
        .join(Organization, Vendor.organization_id == Organization.id)
        .filter(Vendor.active_status == True)
        .all()
    )

    return [
        {
            "id": v.id,
            "organization_name": org.organization_name,
            "vendor_type": v.vendor_type,
            "geographic_coverage": v.geographic_coverage,
            "contract_ready": v.contract_ready,
            "emergency_surge_capable": v.emergency_surge_capable,
            "response_sla_hours": v.response_sla_hours,
            "lead_time_days": v.lead_time_days,
            "active_status": v.active_status,
        }
        for v, org in results
    ]
