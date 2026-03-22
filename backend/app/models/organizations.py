from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from app.models.base import Base, TimestampMixin


class Organization(Base, TimestampMixin):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    organization_name: Mapped[str] = mapped_column(String, nullable=False)
    organization_type: Mapped[str] = mapped_column(String, nullable=False)
    website_url: Mapped[str | None] = mapped_column(String)
    sam_uei: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)
