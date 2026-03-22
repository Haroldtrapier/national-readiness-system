from sqlalchemy import String, ForeignKey, Float, Integer, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from datetime import date
from app.models.base import Base, TimestampMixin


class ItItemCategory(Base, TimestampMixin):
    __tablename__ = "it_item_categories"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    category_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class ItAsset(Base, TimestampMixin):
    __tablename__ = "it_assets"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    agency_id: Mapped[str] = mapped_column(ForeignKey("agencies.id"), nullable=False)
    agency_site_id: Mapped[str | None] = mapped_column(ForeignKey("agency_sites.id"))
    asset_tag: Mapped[str | None] = mapped_column(String)
    asset_type: Mapped[str] = mapped_column(String, nullable=False)
    manufacturer: Mapped[str | None] = mapped_column(String)
    model: Mapped[str | None] = mapped_column(String)
    serial_number: Mapped[str | None] = mapped_column(String)
    operating_system: Mapped[str | None] = mapped_column(String)
    purchase_date: Mapped[date | None] = mapped_column(Date)
    warranty_end_date: Mapped[date | None] = mapped_column(Date)
    assigned_user: Mapped[str | None] = mapped_column(String)
    operating_status: Mapped[str | None] = mapped_column(String)
    security_status: Mapped[str | None] = mapped_column(String)
    lifecycle_years: Mapped[int | None] = mapped_column(Integer)
    replacement_score: Mapped[float | None] = mapped_column(Float)


class ItDemandForecast(Base, TimestampMixin):
    __tablename__ = "it_demand_forecasts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    agency_id: Mapped[str] = mapped_column(ForeignKey("agencies.id"), nullable=False)
    county_id: Mapped[str | None] = mapped_column(ForeignKey("counties.id"))
    linked_hazard_event_id: Mapped[str | None] = mapped_column(ForeignKey("hazard_events.id"))
    it_item_category_id: Mapped[str] = mapped_column(ForeignKey("it_item_categories.id"), nullable=False)
    quantity_needed: Mapped[int] = mapped_column(Integer, nullable=False)
    date_needed: Mapped[date | None] = mapped_column(Date)
    reason_code: Mapped[str] = mapped_column(String, nullable=False)
    confidence_score: Mapped[float | None] = mapped_column(Float)
    procurement_action_score: Mapped[float | None] = mapped_column(Float)
    notes: Mapped[str | None] = mapped_column(Text)


class ContractVehicle(Base, TimestampMixin):
    __tablename__ = "contract_vehicles"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    vehicle_name: Mapped[str] = mapped_column(String, nullable=False)
    vehicle_type: Mapped[str] = mapped_column(String, nullable=False)
    eligible_buyer_types: Mapped[str | None] = mapped_column(String)
    categories: Mapped[str | None] = mapped_column(String)
    jurisdiction_scope: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)


class AgencyContractEligibility(Base, TimestampMixin):
    __tablename__ = "agency_contract_eligibility"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    agency_id: Mapped[str] = mapped_column(ForeignKey("agencies.id"), nullable=False)
    contract_vehicle_id: Mapped[str] = mapped_column(ForeignKey("contract_vehicles.id"), nullable=False)
    eligibility_status: Mapped[str] = mapped_column(String, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)
