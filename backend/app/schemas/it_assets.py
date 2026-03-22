from pydantic import BaseModel
from datetime import date


class ItAssetOut(BaseModel):
    id: str
    asset_tag: str | None = None
    asset_type: str
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    operating_system: str | None = None
    purchase_date: date | None = None
    warranty_end_date: date | None = None
    assigned_user: str | None = None
    operating_status: str | None = None
    security_status: str | None = None
    replacement_score: float | None = None
    agency_name: str | None = None
    site_name: str | None = None

    class Config:
        from_attributes = True


class ItDemandForecastOut(BaseModel):
    id: str
    agency_name: str | None = None
    item_category: str
    quantity_needed: int
    date_needed: date | None = None
    reason_code: str
    confidence_score: float | None = None
    procurement_action_score: float | None = None
    notes: str | None = None

    class Config:
        from_attributes = True


class ItSurgeResult(BaseModel):
    laptops: int
    hotspots: int
    printers: int
    tablets: int
    monitors: int
    trigger: str
    jurisdiction: str


class AgencyItSummary(BaseModel):
    agency_id: str
    agency_name: str
    total_assets: int
    expiring_warranty_90d: int
    high_risk_replacements: int
    surge_devices_needed: int
    assets: list[ItAssetOut] = []
    forecasts: list[ItDemandForecastOut] = []
