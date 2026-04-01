from sqlalchemy import String, ForeignKey, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from app.models.base import Base, TimestampMixin


class Poc(Base, TimestampMixin):
    __tablename__ = "pocs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str | None] = mapped_column(ForeignKey("organizations.id"))
    contact_name: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)
    mobile_phone: Mapped[str | None] = mapped_column(String)
    contact_type: Mapped[str] = mapped_column(String, nullable=False)
    availability_type: Mapped[str | None] = mapped_column(String)
    escalation_level: Mapped[int] = mapped_column(Integer, default=1)
    state_id: Mapped[str | None] = mapped_column(ForeignKey("states.id"))
    county_id: Mapped[str | None] = mapped_column(ForeignKey("counties.id"))
    fema_region_id: Mapped[str | None] = mapped_column(ForeignKey("fema_regions.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(Text)
