from pydantic import BaseModel


class VendorOut(BaseModel):
    id: str
    organization_name: str
    vendor_type: str
    geographic_coverage: str | None = None
    contract_ready: bool = False
    emergency_surge_capable: bool = False
    response_sla_hours: int | None = None
    lead_time_days: int | None = None
    active_status: bool = True

    class Config:
        from_attributes = True


class VendorMatchOut(BaseModel):
    id: str
    match_type: str
    vendor_name: str
    vendor_type: str
    fit_score: float
    delivery_risk_score: float | None = None
    ranking_reason: str | None = None

    class Config:
        from_attributes = True


class VendorSearchParams(BaseModel):
    item_type: str | None = None
    region_number: int | None = None
    state_code: str | None = None
    contract_ready: bool | None = None
    emergency_surge: bool | None = None
