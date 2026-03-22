from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.contacts import Poc
from app.models.organizations import Organization
from app.models.geography import FemaRegion, State, County

router = APIRouter(prefix="/pocs", tags=["Points of Contact"])


def _poc_to_dict(poc: Poc, org: Organization | None) -> dict:
    return {
        "id": poc.id,
        "organization_name": org.organization_name if org else None,
        "contact_name": poc.contact_name,
        "title": poc.title,
        "email": poc.email,
        "phone": poc.phone,
        "mobile_phone": poc.mobile_phone,
        "contact_type": poc.contact_type,
        "availability_type": poc.availability_type,
        "escalation_level": poc.escalation_level,
        "is_active": poc.is_active,
    }


@router.get("/fema/{region_number}")
def fema_pocs(region_number: int, db: Session = Depends(get_db)):
    region = db.query(FemaRegion).filter(FemaRegion.region_number == region_number).first()
    if not region:
        return {"error": "Region not found"}

    results = (
        db.query(Poc, Organization)
        .outerjoin(Organization, Poc.organization_id == Organization.id)
        .filter(Poc.fema_region_id == region.id)
        .filter(Poc.is_active == True)
        .order_by(Poc.escalation_level)
        .all()
    )

    return [_poc_to_dict(p, org) for p, org in results]


@router.get("/sema/{state_code}")
def sema_pocs(state_code: str, db: Session = Depends(get_db)):
    state = db.query(State).filter(State.state_code == state_code.upper()).first()
    if not state:
        return {"error": "State not found"}

    results = (
        db.query(Poc, Organization)
        .outerjoin(Organization, Poc.organization_id == Organization.id)
        .filter(Poc.state_id == state.id)
        .filter(Poc.is_active == True)
        .order_by(Poc.escalation_level)
        .all()
    )

    return [_poc_to_dict(p, org) for p, org in results]


@router.get("/local/{county_fips}")
def local_pocs(county_fips: str, db: Session = Depends(get_db)):
    county = db.query(County).filter(County.county_fips == county_fips).first()
    if not county:
        return {"error": "County not found"}

    results = (
        db.query(Poc, Organization)
        .outerjoin(Organization, Poc.organization_id == Organization.id)
        .filter(Poc.county_id == county.id)
        .filter(Poc.is_active == True)
        .order_by(Poc.escalation_level)
        .all()
    )

    return [_poc_to_dict(p, org) for p, org in results]


@router.get("/all")
def all_pocs(
    contact_type: str | None = None,
    state_code: str | None = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Poc, Organization)
        .outerjoin(Organization, Poc.organization_id == Organization.id)
        .filter(Poc.is_active == True)
    )

    if contact_type:
        query = query.filter(Poc.contact_type == contact_type)

    if state_code:
        state = db.query(State).filter(State.state_code == state_code.upper()).first()
        if state:
            query = query.filter(Poc.state_id == state.id)

    results = query.order_by(Poc.escalation_level).all()
    return [_poc_to_dict(p, org) for p, org in results]
