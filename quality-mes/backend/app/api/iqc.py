from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database import get_db
from app.models.iqc import IQCInspection, IQCResult, Material, Supplier
from app.schemas.iqc import (
    IQCInspectionCreate,
    IQCInspectionResponse,
    IQCResultCreate,
    IQCResultResponse,
    MaterialCreate,
    MaterialResponse,
    SupplierCreate,
    SupplierResponse,
)

router = APIRouter(prefix="/api/iqc", tags=["IQC"])


# ---- Suppliers ----
@router.get("/suppliers", response_model=list[SupplierResponse])
def list_suppliers(
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(Supplier)
    if search:
        query = query.filter(
            (Supplier.name.contains(search)) | (Supplier.code.contains(search))
        )
    return query.order_by(Supplier.name).all()


@router.post("/suppliers", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    existing = db.query(Supplier).filter(Supplier.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ma nha cung cap da ton tai")
    obj = Supplier(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    data: SupplierCreate,
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    obj = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay nha cung cap")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/suppliers/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay nha cung cap")
    db.delete(obj)
    db.commit()


# ---- Materials ----
@router.get("/materials", response_model=list[MaterialResponse])
def list_materials(
    search: str | None = Query(None),
    supplier_id: int | None = Query(None),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(Material)
    if search:
        query = query.filter(
            (Material.name.contains(search)) | (Material.code.contains(search))
        )
    if supplier_id:
        query = query.filter(Material.supplier_id == supplier_id)
    return query.order_by(Material.name).all()


@router.post("/materials", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
def create_material(data: MaterialCreate, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    existing = db.query(Material).filter(Material.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ma nguyen lieu da ton tai")
    supplier = db.query(Supplier).filter(Supplier.id == data.supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=400, detail="Nha cung cap khong ton tai")
    obj = Material(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/materials/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_material(material_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(Material).filter(Material.id == material_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay nguyen lieu")
    db.delete(obj)
    db.commit()


# ---- Inspections ----
@router.get("/inspections", response_model=list[IQCInspectionResponse])
def list_inspections(
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(IQCInspection)
    if status:
        query = query.filter(IQCInspection.status == status)
    total = query.count()
    inspections = query.order_by(IQCInspection.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return inspections


@router.post("/inspections", response_model=IQCInspectionResponse, status_code=status.HTTP_201_CREATED)
def create_inspection(
    data: IQCInspectionCreate,
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    existing = db.query(IQCInspection).filter(IQCInspection.inspection_no == data.inspection_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="So phieu kiem tra da ton tai")
    obj = IQCInspection(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/inspections/{inspection_id}", response_model=IQCInspectionResponse)
def get_inspection(inspection_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(IQCInspection).filter(IQCInspection.id == inspection_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu kiem tra")
    return obj


@router.put("/inspections/{inspection_id}/status")
def update_inspection_status(
    inspection_id: int,
    status: str = Query(..., pattern="^(pending|pass|fail)$"),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    obj = db.query(IQCInspection).filter(IQCInspection.id == inspection_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu kiem tra")
    obj.status = status
    db.commit()
    return {"message": "Cap nhat trang thai thanh cong", "status": status}


# ---- Results ----
@router.post("/inspections/{inspection_id}/results", response_model=IQCResultResponse, status_code=status.HTTP_201_CREATED)
def add_result(
    inspection_id: int,
    data: IQCResultCreate,
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    inspection = db.query(IQCInspection).filter(IQCInspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu kiem tra")
    obj = IQCResult(inspection_id=inspection_id, **data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/results/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(result_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(IQCResult).filter(IQCResult.id == result_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay ket qua")
    db.delete(obj)
    db.commit()
