from datetime import datetime
from pydantic import BaseModel, Field


class IPQCResultCreate(BaseModel):
    item_name: str
    specification: str | None = None
    measured_value: float
    standard_min: float | None = None
    standard_max: float | None = None
    result: str = "pass"
    notes: str | None = None


class IPQCResultResponse(BaseModel):
    id: int
    inspection_id: int
    item_name: str
    specification: str | None = None
    measured_value: float
    standard_min: float | None = None
    standard_max: float | None = None
    result: str
    notes: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserBrief(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

    model_config = {"from_attributes": True}


class IPQCInspectionCreate(BaseModel):
    inspection_no: str
    process_name: str
    work_center: str
    machine: str | None = None
    shift: str = "Ca 1"
    inspection_date: datetime
    inspector_id: int
    sample_size: int = 5
    notes: str | None = None


class IPQCInspectionResponse(BaseModel):
    id: int
    inspection_no: str
    process_name: str
    work_center: str
    machine: str | None = None
    shift: str
    inspection_date: datetime
    inspector_id: int
    sample_size: int
    status: str
    notes: str | None = None
    inspector: UserBrief | None = None
    results: list[IPQCResultResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}
