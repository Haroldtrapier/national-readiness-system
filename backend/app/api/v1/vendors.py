from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.vendor_matching_service import get_all_vendors, find_vendors_for_item

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("")
def list_vendors(db: Session = Depends(get_db)):
    return get_all_vendors(db)


@router.get("/matches/supply")
def match_supply_vendors(
    item_name: str,
    state_code: str | None = None,
    db: Session = Depends(get_db),
):
    matches = find_vendors_for_item(item_name, state_code, db)
    return {"item_name": item_name, "matches": matches}


@router.get("/by-region/{region_number}")
def vendors_by_region(region_number: int, db: Session = Depends(get_db)):
    from app.models.vendors import Vendor, Organization
    from app.models.geography import State, FemaRegion

    region = db.query(FemaRegion).filter(FemaRegion.region_number == region_number).first()
    if not region:
        return {"error": "Region not found"}

    states = db.query(State).filter(State.fema_region_id == region.id).all()
    state_ids = [s.id for s in states]

    vendors = (
        db.query(Vendor, Organization)
        .join(Organization, Vendor.organization_id == Organization.id)
        .filter(Vendor.primary_state_id.in_(state_ids))
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
        }
        for v, org in vendors
    ]
