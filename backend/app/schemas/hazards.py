from pydantic import BaseModel
from datetime import datetime


class HazardTypeOut(BaseModel):
    id: str
    hazard_code: str
    hazard_name: str
    category: str
    description: str | None = None

    class Config:
        from_attributes = True


class HazardSummary(BaseModel):
    hazard_code: str
    hazard_name: str
    region_number: int | None = None
    state_code: str | None = None
    county_name: str | None = None
    county_fips: str | None = None
    probability_score: float | None = None
    severity_score: float | None = None
    confidence_score: float | None = None
    readiness_band: str | None = None
    confidence_band: str | None = None


class NationalHazardResponse(BaseModel):
    active_hazards: int
    counties_at_risk: int
    top_hazards: list[HazardSummary]
    timestamp: datetime


class RegionHazardResponse(BaseModel):
    region_number: int
    region_name: str
    active_hazards: int
    counties_at_risk: int
    readiness_band: str
    hazards: list[HazardSummary]


class HazardEventOut(BaseModel):
    id: str
    hazard_type_id: str
    event_source: str
    event_name: str | None = None
    event_status: str
    probability_score: float | None = None
    severity_score: float | None = None
    confidence_score: float | None = None
    issued_at: datetime | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None

    class Config:
        from_attributes = True
