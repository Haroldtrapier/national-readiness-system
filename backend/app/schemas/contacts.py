from pydantic import BaseModel


class PocOut(BaseModel):
    id: str
    organization_name: str | None = None
    contact_name: str
    title: str | None = None
    email: str | None = None
    phone: str | None = None
    mobile_phone: str | None = None
    contact_type: str
    availability_type: str | None = None
    escalation_level: int = 1
    state_code: str | None = None
    county_name: str | None = None
    fema_region_number: int | None = None
    is_active: bool = True

    class Config:
        from_attributes = True


class PocCreate(BaseModel):
    organization_id: str | None = None
    contact_name: str
    title: str | None = None
    email: str | None = None
    phone: str | None = None
    mobile_phone: str | None = None
    contact_type: str
    availability_type: str | None = None
    escalation_level: int = 1
    state_id: str | None = None
    county_id: str | None = None
    fema_region_id: str | None = None
    notes: str | None = None
