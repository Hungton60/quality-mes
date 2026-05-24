from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database import get_db
from app.models.oqc import OQCInspection, OQCResult, Product
from app.schemas.oqc import (
    OQCInspectionCreate,
    OQCInspectionResponse,
    OQCResultCreate,
    OQCResultResponse,
    ProductCreate,
    ProductResponse,
)

router = APIRouter(prefix="/api/oqc", tags=["OQC"])


# ---- Products ----
@router.get("/products", response_model=list[ProductResponse])
def list_products(
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(Product)
    if search:
        query = query.filter(
            (Product.name.contains(search)) | (Product.code.contains(search))
        )
    return query.order_by(Product.name).all()


@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    existing = db.query(Product).filter(Product.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ma san pham da ton tai")
    obj = Product(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(Product).filter(Product.id == product_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay san pham")
    db.delete(obj)
    db.commit()


# ---- Inspections ----
@router.get("/inspections", response_model=list[OQCInspectionResponse])
def list_inspections(
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(OQCInspection)
    if status:
        query = query.filter(OQCInspection.status == status)
    inspections = query.order_by(OQCInspection.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return inspections


@router.post("/inspections", response_model=OQCInspectionResponse, status_code=status.HTTP_201_CREATED)
def create_inspection(
    data: OQCInspectionCreate,
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    existing = db.query(OQCInspection).filter(OQCInspection.inspection_no == data.inspection_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="So phieu kiem tra da ton tai")
    obj = OQCInspection(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/inspections/{inspection_id}", response_model=OQCInspectionResponse)
def get_inspection(inspection_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(OQCInspection).filter(OQCInspection.id == inspection_id).first()
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
    obj = db.query(OQCInspection).filter(OQCInspection.id == inspection_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu kiem tra")
    obj.status = status
    db.commit()
    return {"message": "Cap nhat trang thai thanh cong", "status": status}


# ---- Results ----
@router.post("/inspections/{inspection_id}/results", response_model=OQCResultResponse, status_code=status.HTTP_201_CREATED)
def add_result(
    inspection_id: int,
    data: OQCResultCreate,
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    inspection = db.query(OQCInspection).filter(OQCInspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu kiem tra")
    obj = OQCResult(inspection_id=inspection_id, **data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/results/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(result_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(OQCResult).filter(OQCResult.id == result_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay ket qua")
    db.delete(obj)
    db.commit()
