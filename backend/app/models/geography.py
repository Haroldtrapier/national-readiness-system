from sqlalchemy import String, Boolean, ForeignKey, Integer, Float, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import uuid4
from app.models.base import Base, TimestampMixin


class FemaRegion(Base, TimestampMixin):
    __tablename__ = "fema_regions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    region_number: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    region_name: Mapped[str] = mapped_column(String, nullable=False)
    headquarters_city: Mapped[str | None] = mapped_column(String)
    headquarters_state: Mapped[str | None] = mapped_column(String)

    states: Mapped[list["State"]] = relationship(back_populates="fema_region")


class State(Base, TimestampMixin):
    __tablename__ = "states"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    state_code: Mapped[str] = mapped_column(String(2), unique=True, nullable=False)
    state_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    fema_region_id: Mapped[str | None] = mapped_column(ForeignKey("fema_regions.id"))
    is_territory: Mapped[bool] = mapped_column(Boolean, default=False)

    fema_region: Mapped[FemaRegion | None] = relationship(back_populates="states")
    counties: Mapped[list["County"]] = relationship(back_populates="state")


class County(Base, TimestampMixin):
    __tablename__ = "counties"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    state_id: Mapped[str] = mapped_column(ForeignKey("states.id"), nullable=False)
    county_name: Mapped[str] = mapped_column(String, nullable=False)
    county_fips: Mapped[str | None] = mapped_column(String(5), unique=True)
    population: Mapped[int | None] = mapped_column(BigInteger)
    is_coastal: Mapped[bool] = mapped_column(Boolean, default=False)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)

    state: Mapped[State] = relationship(back_populates="counties")
