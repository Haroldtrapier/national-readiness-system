from pydantic import BaseModel
from datetime import datetime


class ThreatBriefItem(BaseModel):
    hazard_type: str
    area: str
    risk_level: str
    confidence: str
    narrative: str


class SupplyBriefItem(BaseModel):
    item_name: str
    required: float
    available: float
    shortage: float
    shortage_pct: float


class VendorBriefItem(BaseModel):
    vendor_name: str
    capability: str
    sla_hours: int | None = None
    contract_ready: bool = False


class PocBriefItem(BaseModel):
    name: str
    role: str
    phone: str | None = None
    email: str | None = None
    availability: str | None = None


class OperationalBrief(BaseModel):
    title: str
    scope: str
    generated_at: datetime
    readiness_band: str
    threats: list[ThreatBriefItem]
    supply_needs: list[SupplyBriefItem]
    recommended_vendors: list[VendorBriefItem]
    key_contacts: list[PocBriefItem]
    it_surge_needs: dict | None = None
    recommended_actions: list[str]
