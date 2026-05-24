from datetime import datetime
from pydantic import BaseModel, Field


class UserBrief(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

    model_config = {"from_attributes": True}


# ---- Product ----
class ProductCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    specification: str | None = None
    unit: str = "pcs"


class ProductResponse(BaseModel):
    id: int
    code: str
    name: str
    specification: str | None = None
    unit: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ---- OQC Result ----
class OQCResultCreate(BaseModel):
    item_name: str
    specification: str | None = None
    measured_value: float
    standard_min: float | None = None
    standard_max: float | None = None
    result: str = "pass"
    notes: str | None = None


class OQCResultResponse(BaseModel):
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


# ---- OQC Inspection ----
class OQCInspectionCreate(BaseModel):
    inspection_no: str
    product_id: int
    lot_no: str
    quantity: int
    sample_size: int
    inspection_date: datetime
    inspector_id: int
    notes: str | None = None


class OQCInspectionResponse(BaseModel):
    id: int
    inspection_no: str
    product_id: int
    lot_no: str
    quantity: int
    sample_size: int
    inspection_date: datetime
    inspector_id: int
    status: str
    notes: str | None = None
    product: ProductResponse | None = None
    inspector: UserBrief | None = None
    results: list[OQCResultResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}
