from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class NCR(Base):
    __tablename__ = "ncrs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ncr_no: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default="minor")  # critical, major, minor
    source_type: Mapped[str] = mapped_column(String(20), nullable=True)  # iqc, ipqc, oqc, other
    source_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    reported_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    assigned_to: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, investigating, resolved, closed
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resolution: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    reporter: Mapped["User"] = relationship(foreign_keys=[reported_by], lazy="selectin")
    assignee: Mapped["User | None"] = relationship(foreign_keys=[assigned_to], lazy="selectin")
    capas: Mapped[list["CAPA"]] = relationship(back_populates="ncr", lazy="selectin", cascade="all, delete-orphan")


class CAPA(Base):
    __tablename__ = "capas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    capa_no: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    ncr_id: Mapped[int] = mapped_column(Integer, ForeignKey("ncrs.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False, default="corrective")  # corrective, preventive
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    root_cause: Mapped[str | None] = mapped_column(Text)
    action_plan: Mapped[str | None] = mapped_column(Text)
    assigned_to: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="open")  # open, in_progress, completed, verified
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    verified_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    effectiveness: Mapped[str | None] = mapped_column(String(50))  # effective, partially_effective, ineffective
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    ncr: Mapped["NCR"] = relationship(back_populates="capas")
    assignee: Mapped["User | None"] = relationship(foreign_keys=[assigned_to], lazy="selectin")
    verifier: Mapped["User | None"] = relationship(foreign_keys=[verified_by], lazy="selectin")
