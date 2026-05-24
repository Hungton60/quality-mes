from datetime import datetime
from pydantic import BaseModel, Field


class UserBrief(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

    model_config = {"from_attributes": True}


# ---- Supplier ----
class SupplierCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None


class SupplierResponse(BaseModel):
    id: int
    code: str
    name: str
    contact_person: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ---- Material ----
class MaterialCreate(BaseModel):
    code: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    specification: str | None = None
    unit: str = "pcs"
    supplier_id: int


class MaterialResponse(BaseModel):
    id: int
    code: str
    name: str
    specification: str | None = None
    unit: str
    supplier_id: int
    supplier: SupplierResponse | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ---- IQC Result ----
class IQCResultCreate(BaseModel):
    item_name: str
    specification: str | None = None
    measured_value: float
    standard_min: float | None = None
    standard_max: float | None = None
    result: str = "pass"
    notes: str | None = None


class IQCResultResponse(BaseModel):
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


# ---- IQC Inspection ----
class IQCInspectionCreate(BaseModel):
    inspection_no: str
    material_id: int
    supplier_id: int
    lot_no: str
    quantity: int
    sample_size: int
    inspection_date: datetime
    inspector_id: int
    notes: str | None = None


class IQCInspectionResponse(BaseModel):
    id: int
    inspection_no: str
    material_id: int
    supplier_id: int
    lot_no: str
    quantity: int
    sample_size: int
    inspection_date: datetime
    inspector_id: int
    status: str
    notes: str | None = None
    material: MaterialResponse | None = None
    supplier: SupplierResponse | None = None
    inspector: UserBrief | None = None
    results: list[IQCResultResponse] = []
    created_at: datetime

    model_config = {"from_attributes": True}
