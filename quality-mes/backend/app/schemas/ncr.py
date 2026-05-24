from datetime import datetime
from pydantic import BaseModel, Field


class UserBrief(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    model_config = {"from_attributes": True}


# ---- CAPA ----
class CAPACreate(BaseModel):
    capa_no: str
    ncr_id: int
    type: str = "corrective"
    title: str
    description: str
    root_cause: str | None = None
    action_plan: str | None = None
    assigned_to: int | None = None
    status: str = "open"
    due_date: datetime | None = None
    completed_date: datetime | None = None
    verified_by: int | None = None
    effectiveness: str | None = None


class CAPAResponse(BaseModel):
    id: int
    capa_no: str
    ncr_id: int
    type: str
    title: str
    description: str
    root_cause: str | None = None
    action_plan: str | None = None
    assigned_to: int | None = None
    status: str
    due_date: datetime | None = None
    completed_date: datetime | None = None
    verified_by: int | None = None
    effectiveness: str | None = None
    assignee: UserBrief | None = None
    verifier: UserBrief | None = None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


# ---- NCR ----
class NCRCreate(BaseModel):
    ncr_no: str
    title: str
    description: str
    severity: str = "minor"
    source_type: str | None = None
    source_id: int | None = None
    reported_by: int
    assigned_to: int | None = None
    due_date: datetime | None = None


class NCRResponse(BaseModel):
    id: int
    ncr_no: str
    title: str
    description: str
    severity: str
    source_type: str | None = None
    source_id: int | None = None
    reported_by: int
    assigned_to: int | None = None
    status: str
    due_date: datetime | None = None
    resolution: str | None = None
    reporter: UserBrief | None = None
    assignee: UserBrief | None = None
    capas: list[CAPAResponse] = []
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}
