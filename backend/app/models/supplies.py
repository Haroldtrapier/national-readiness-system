from sqlalchemy import String, ForeignKey, Float, Text, Boolean, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from app.models.base import Base, TimestampMixin


class SupplyCategory(Base, TimestampMixin):
    __tablename__ = "supply_categories"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    category_code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)


class SupplyItem(Base, TimestampMixin):
    __tablename__ = "supply_items"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    sku_code: Mapped[str | None] = mapped_column(String, unique=True)
    item_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    supply_category_id: Mapped[str | None] = mapped_column(ForeignKey("supply_categories.id"))
    unit_of_measure: Mapped[str] = mapped_column(String, nullable=False)
    item_description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class SupplyPackage(Base, TimestampMixin):
    __tablename__ = "supply_packages"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    hazard_code: Mapped[str] = mapped_column(String, nullable=False)
    severity_band: Mapped[str] = mapped_column(String, nullable=False)
    package_name: Mapped[str] = mapped_column(String, nullable=False)


class SupplyPackageItem(Base):
    __tablename__ = "supply_package_items"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    supply_package_id: Mapped[str] = mapped_column(ForeignKey("supply_packages.id"), nullable=False)
    supply_item_id: Mapped[str] = mapped_column(ForeignKey("supply_items.id"), nullable=False)
    default_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)


class SupplyRequirement(Base, TimestampMixin):
    __tablename__ = "supply_requirements"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    readiness_assessment_id: Mapped[str] = mapped_column(ForeignKey("readiness_assessments.id"), nullable=False)
    supply_item_id: Mapped[str] = mapped_column(ForeignKey("supply_items.id"), nullable=False)
    required_quantity: Mapped[float] = mapped_column(Float, nullable=False)
    available_quantity: Mapped[float | None] = mapped_column(Float)
    shortage_quantity: Mapped[float | None] = mapped_column(Float)
    priority_level: Mapped[str | None] = mapped_column(String)
