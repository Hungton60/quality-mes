from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    specification: Mapped[str | None] = mapped_column(Text)
    unit: Mapped[str] = mapped_column(String(20), default="pcs")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class OQCInspection(Base):
    __tablename__ = "oqc_inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inspection_no: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    lot_no: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    inspection_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    inspector_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, pass, fail
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    product: Mapped["Product"] = relationship(lazy="selectin")
    inspector: Mapped["User"] = relationship(lazy="selectin")
    results: Mapped[list["OQCResult"]] = relationship(back_populates="inspection", lazy="selectin", cascade="all, delete-orphan")


class OQCResult(Base):
    __tablename__ = "oqc_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inspection_id: Mapped[int] = mapped_column(Integer, ForeignKey("oqc_inspections.id"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(200), nullable=False)
    specification: Mapped[str | None] = mapped_column(String(200))
    measured_value: Mapped[float] = mapped_column(nullable=False)
    standard_min: Mapped[float | None] = mapped_column()
    standard_max: Mapped[float | None] = mapped_column()
    result: Mapped[str] = mapped_column(String(10), default="pass")  # pass, fail
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    inspection: Mapped["OQCInspection"] = relationship(back_populates="results")
