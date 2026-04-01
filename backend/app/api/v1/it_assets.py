from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.it_lifecycle_service import get_agency_it_summary, get_state_it_forecast

router = APIRouter(prefix="/it-assets", tags=["IT Assets"])


@router.get("/agencies/{agency_id}")
def agency_assets(agency_id: str, db: Session = Depends(get_db)):
    return get_agency_it_summary(agency_id, db)


@router.get("/forecast/states/{state_code}")
def state_forecast(state_code: str, db: Session = Depends(get_db)):
    forecasts = get_state_it_forecast(state_code, db)
    return {"state_code": state_code, "forecasts": forecasts}


@router.get("/forecast/regions/{region_number}")
def region_forecast(region_number: int, db: Session = Depends(get_db)):
    from app.models.geography import FemaRegion, State
    from app.models.agencies import Agency
    from app.models.organizations import Organization
    from app.models.it_assets import ItDemandForecast, ItItemCategory

    region = db.query(FemaRegion).filter(FemaRegion.region_number == region_number).first()
    if not region:
        return {"error": "Region not found"}

    states = db.query(State).filter(State.fema_region_id == region.id).all()
    state_ids = [s.id for s in states]
    agencies = db.query(Agency).filter(Agency.state_id.in_(state_ids)).all()
    agency_ids = [a.id for a in agencies]

    forecasts = (
        db.query(ItDemandForecast, ItItemCategory, Agency, Organization)
        .join(ItItemCategory, ItDemandForecast.it_item_category_id == ItItemCategory.id)
        .join(Agency, ItDemandForecast.agency_id == Agency.id)
        .join(Organization, Agency.organization_id == Organization.id)
        .filter(ItDemandForecast.agency_id.in_(agency_ids))
        .all()
    )

    return {
        "region_number": region_number,
        "forecasts": [
            {
                "agency_name": org.organization_name,
                "item_category": cat.category_name,
                "quantity_needed": f.quantity_needed,
                "date_needed": f.date_needed.isoformat() if f.date_needed else None,
                "reason_code": f.reason_code,
                "confidence_score": f.confidence_score,
            }
            for f, cat, ag, org in forecasts
        ],
    }
