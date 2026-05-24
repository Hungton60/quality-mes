from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class IPQCInspection(Base):
    __tablename__ = "ipqc_inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inspection_no: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    process_name: Mapped[str] = mapped_column(String(200), nullable=False)
    work_center: Mapped[str] = mapped_column(String(100), nullable=False)
    machine: Mapped[str | None] = mapped_column(String(100))
    shift: Mapped[str] = mapped_column(String(20), default="Ca 1")
    inspection_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    inspector_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    sample_size: Mapped[int] = mapped_column(Integer, default=5)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    inspector: Mapped["User"] = relationship(lazy="selectin")
    results: Mapped[list["IPQCResult"]] = relationship(back_populates="inspection", lazy="selectin", cascade="all, delete-orphan")


class IPQCResult(Base):
    __tablename__ = "ipqc_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    inspection_id: Mapped[int] = mapped_column(Integer, ForeignKey("ipqc_inspections.id"), nullable=False)
    item_name: Mapped[str] = mapped_column(String(200), nullable=False)
    specification: Mapped[str | None] = mapped_column(String(200))
    measured_value: Mapped[float] = mapped_column(nullable=False)
    standard_min: Mapped[float | None] = mapped_column()
    standard_max: Mapped[float | None] = mapped_column()
    result: Mapped[str] = mapped_column(String(10), default="pass")
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    inspection: Mapped["IPQCInspection"] = relationship(back_populates="results")
