from pydantic import BaseModel


class FemaRegionOut(BaseModel):
    id: str
    region_number: int
    region_name: str
    headquarters_city: str | None = None
    headquarters_state: str | None = None

    class Config:
        from_attributes = True


class StateOut(BaseModel):
    id: str
    state_code: str
    state_name: str
    fema_region_id: str | None = None
    is_territory: bool = False

    class Config:
        from_attributes = True


class CountyOut(BaseModel):
    id: str
    state_id: str
    county_name: str
    county_fips: str | None = None
    population: int | None = None
    is_coastal: bool = False
    latitude: float | None = None
    longitude: float | None = None

    class Config:
        from_attributes = True
