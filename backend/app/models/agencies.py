from sqlalchemy import String, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from app.models.base import Base, TimestampMixin


class Agency(Base, TimestampMixin):
    __tablename__ = "agencies"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    agency_level: Mapped[str] = mapped_column(String, nullable=False)
    state_id: Mapped[str | None] = mapped_column(ForeignKey("states.id"))
    county_id: Mapped[str | None] = mapped_column(ForeignKey("counties.id"))
    fema_region_id: Mapped[str | None] = mapped_column(ForeignKey("fema_regions.id"))
    mission_type: Mapped[str | None] = mapped_column(String)
    procurement_owner_poc_id: Mapped[str | None] = mapped_column(ForeignKey("pocs.id"))
    emergency_owner_poc_id: Mapped[str | None] = mapped_column(ForeignKey("pocs.id"))
    it_owner_poc_id: Mapped[str | None] = mapped_column(ForeignKey("pocs.id"))
    active_status: Mapped[bool] = mapped_column(Boolean, default=True)


class AgencySite(Base, TimestampMixin):
    __tablename__ = "agency_sites"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    agency_id: Mapped[str] = mapped_column(ForeignKey("agencies.id"), nullable=False)
    site_name: Mapped[str] = mapped_column(String, nullable=False)
    site_type: Mapped[str] = mapped_column(String, nullable=False)
    address_line_1: Mapped[str | None] = mapped_column(String)
    city: Mapped[str | None] = mapped_column(String)
    state_code: Mapped[str | None] = mapped_column(String(2))
    postal_code: Mapped[str | None] = mapped_column(String)
    county_name: Mapped[str | None] = mapped_column(String)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    continuity_criticality: Mapped[str | None] = mapped_column(String)
