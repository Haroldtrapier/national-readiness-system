from sqlalchemy import String, ForeignKey, Float, Text, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from datetime import datetime
from app.models.base import Base, TimestampMixin


class HazardType(Base, TimestampMixin):
    __tablename__ = "hazard_types"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    hazard_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hazard_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class HazardEvent(Base, TimestampMixin):
    __tablename__ = "hazard_events"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    hazard_type_id: Mapped[str] = mapped_column(ForeignKey("hazard_types.id"), nullable=False)
    event_source: Mapped[str] = mapped_column(String, nullable=False)
    external_event_id: Mapped[str | None] = mapped_column(String)
    event_name: Mapped[str | None] = mapped_column(String)
    event_status: Mapped[str] = mapped_column(String, default="active")
    probability_score: Mapped[float | None] = mapped_column(Float)
    severity_score: Mapped[float | None] = mapped_column(Float)
    confidence_score: Mapped[float | None] = mapped_column(Float)
    issued_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    source_payload: Mapped[dict | None] = mapped_column(JSON)


class CountyHazardImpact(Base, TimestampMixin):
    __tablename__ = "county_hazard_impacts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    county_id: Mapped[str] = mapped_column(ForeignKey("counties.id"), nullable=False)
    hazard_event_id: Mapped[str] = mapped_column(ForeignKey("hazard_events.id"), nullable=False)
    probability_score: Mapped[float] = mapped_column(Float, nullable=False)
    severity_score: Mapped[float] = mapped_column(Float, nullable=False)
    exposure_score: Mapped[float | None] = mapped_column(Float)
    vulnerability_score: Mapped[float | None] = mapped_column(Float)
    hazard_score: Mapped[float | None] = mapped_column(Float)
    readiness_band: Mapped[str | None] = mapped_column(String)
    confidence_band: Mapped[str | None] = mapped_column(String)


class ReadinessAssessment(Base, TimestampMixin):
    __tablename__ = "readiness_assessments"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    county_id: Mapped[str | None] = mapped_column(ForeignKey("counties.id"))
    state_id: Mapped[str | None] = mapped_column(ForeignKey("states.id"))
    fema_region_id: Mapped[str | None] = mapped_column(ForeignKey("fema_regions.id"))
    hazard_event_id: Mapped[str | None] = mapped_column(ForeignKey("hazard_events.id"))
    readiness_band: Mapped[str] = mapped_column(String, nullable=False)
    hazard_score: Mapped[float] = mapped_column(Float, nullable=False)
    confidence_band: Mapped[str | None] = mapped_column(String)
    action_window: Mapped[str | None] = mapped_column(String)
    narrative: Mapped[str | None] = mapped_column(Text)
