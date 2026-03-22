from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.agencies import Agency, AgencySite
from app.models.organizations import Organization

router = APIRouter(prefix="/agencies", tags=["Agencies"])


@router.get("")
def list_agencies(
    level: str | None = None,
    state_code: str | None = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Agency, Organization)
        .join(Organization, Agency.organization_id == Organization.id)
        .filter(Agency.active_status == True)
    )

    if level:
        query = query.filter(Agency.agency_level == level)

    if state_code:
        from app.models.geography import State
        state = db.query(State).filter(State.state_code == state_code.upper()).first()
        if state:
            query = query.filter(Agency.state_id == state.id)

    results = query.all()
    return [
        {
            "id": a.id,
            "organization_name": org.organization_name,
            "agency_level": a.agency_level,
            "mission_type": a.mission_type,
            "active_status": a.active_status,
        }
        for a, org in results
    ]


@router.get("/{agency_id}")
def get_agency(agency_id: str, db: Session = Depends(get_db)):
    result = (
        db.query(Agency, Organization)
        .join(Organization, Agency.organization_id == Organization.id)
        .filter(Agency.id == agency_id)
        .first()
    )
    if not result:
        return {"error": "Agency not found"}

    a, org = result
    sites = db.query(AgencySite).filter(AgencySite.agency_id == agency_id).all()

    return {
        "id": a.id,
        "organization_name": org.organization_name,
        "agency_level": a.agency_level,
        "mission_type": a.mission_type,
        "sites": [
            {
                "id": s.id,
                "site_name": s.site_name,
                "site_type": s.site_type,
                "city": s.city,
                "state_code": s.state_code,
                "continuity_criticality": s.continuity_criticality,
            }
            for s in sites
        ],
    }
