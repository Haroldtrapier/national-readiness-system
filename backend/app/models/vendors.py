from sqlalchemy import String, ForeignKey, Boolean, Integer, Float, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from app.models.base import Base, TimestampMixin


class Vendor(Base, TimestampMixin):
    __tablename__ = "vendors"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    vendor_type: Mapped[str] = mapped_column(String, nullable=False)
    primary_state_id: Mapped[str | None] = mapped_column(ForeignKey("states.id"))
    geographic_coverage: Mapped[str | None] = mapped_column(String)
    contract_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    emergency_surge_capable: Mapped[bool] = mapped_column(Boolean, default=False)
    response_sla_hours: Mapped[int | None] = mapped_column(Integer)
    lead_time_days: Mapped[int | None] = mapped_column(Integer)
    past_performance_notes: Mapped[str | None] = mapped_column(Text)
    active_status: Mapped[bool] = mapped_column(Boolean, default=True)


class VendorSupplyCapability(Base, TimestampMixin):
    __tablename__ = "vendor_supply_capabilities"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    vendor_id: Mapped[str] = mapped_column(ForeignKey("vendors.id"), nullable=False)
    supply_item_id: Mapped[str | None] = mapped_column(ForeignKey("supply_items.id"))
    it_item_category_id: Mapped[str | None] = mapped_column(ForeignKey("it_item_categories.id"))
    item_type: Mapped[str] = mapped_column(String, nullable=False)
    daily_capacity: Mapped[int | None] = mapped_column(Integer)
    weekly_capacity: Mapped[int | None] = mapped_column(Integer)
    unit_of_measure: Mapped[str | None] = mapped_column(String)
    service_regions: Mapped[dict | None] = mapped_column(JSON)


class VendorMatch(Base, TimestampMixin):
    __tablename__ = "vendor_matches"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    match_type: Mapped[str] = mapped_column(String, nullable=False)
    supply_requirement_id: Mapped[str | None] = mapped_column(ForeignKey("supply_requirements.id"))
    it_demand_forecast_id: Mapped[str | None] = mapped_column(ForeignKey("it_demand_forecasts.id"))
    vendor_id: Mapped[str] = mapped_column(ForeignKey("vendors.id"), nullable=False)
    fit_score: Mapped[float] = mapped_column(Float, nullable=False)
    delivery_risk_score: Mapped[float | None] = mapped_column(Float)
    ranking_reason: Mapped[str | None] = mapped_column(Text)
