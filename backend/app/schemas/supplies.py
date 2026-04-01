from pydantic import BaseModel


class SupplyCategoryOut(BaseModel):
    id: str
    category_code: str
    category_name: str
    description: str | None = None

    class Config:
        from_attributes = True


class SupplyItemOut(BaseModel):
    id: str
    item_name: str
    unit_of_measure: str
    supply_category_id: str | None = None
    is_active: bool = True

    class Config:
        from_attributes = True


class SupplyPackageOut(BaseModel):
    id: str
    hazard_code: str
    severity_band: str
    package_name: str
    items: list[dict] = []

    class Config:
        from_attributes = True


class SupplyRequirementOut(BaseModel):
    id: str
    supply_item_name: str
    required_quantity: float
    available_quantity: float | None = None
    shortage_quantity: float | None = None
    shortage_pct: float | None = None
    priority_level: str | None = None

    class Config:
        from_attributes = True
