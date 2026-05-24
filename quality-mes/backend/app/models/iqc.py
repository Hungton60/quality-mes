from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    contact_person: Mapped[str | None] = mapped_column(String(200))
    phone: Mapped[str | None] = mapped_column(String(20))
    email: Mapped[str | None] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    materials: Mapped[list["Material"]] = relationship(back_populates="supplier", lazy="selectin")
    iqc_inspections: Mapped[list["IQCInspection"]] = relationship(back_populates="supplier", lazy="selectin")


class Material(Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    specification: Mapped[str | None] = mapped_column(Text)
    unit: Mapped[str] = mapped_column(String(20), default="pcs")
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    supplier: Mapped["Supplier"] = relationship(back_populates="materials")


class IQCInspection(Base):
    __tablename__ = "iqc_inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inspection_no: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    material_id: Mapped[int] = mapped_column(Integer, ForeignKey("materials.id"), nullable=False)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey("suppliers.id"), nullable=False)
    lot_no: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, nullable=False)
    inspection_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    inspector_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, pass, fail
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    material: Mapped["Material"] = relationship(lazy="selectin")
    supplier: Mapped["Supplier"] = relationship(back_populates="iqc_inspections")
    inspector: Mapped["User"] = relationship(lazy="selectin")
    results: Mapped[list["IQCResult"]] = relationship(back_populates="inspection", lazy="selectin", cascade="all, delete-orphan")


class IQCResult(Base):
    __tablename__ = "iqc_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inspection_id: Mapped[int] = mapped_column(Integer, ForeignKey("iqc_inspections.id"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(200), nullable=False)
    specification: Mapped[str | None] = mapped_column(String(200))
    measured_value: Mapped[float] = mapped_column(nullable=False)
    standard_min: Mapped[float | None] = mapped_column()
    standard_max: Mapped[float | None] = mapped_column()
    result: Mapped[str] = mapped_column(String(10), default="pass")  # pass, fail
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    inspection: Mapped["IQCInspection"] = relationship(back_populates="results")
