from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database import get_db
from app.models.ipqc import IPQCInspection, IPQCResult
from app.schemas.ipqc import (
    IPQCInspectionCreate,
    IPQCInspectionResponse,
    IPQCResultCreate,
    IPQCResultResponse,
)

router = APIRouter(prefix="/api/ipqc", tags=["IPQC"])


@router.get("/inspections", response_model=list[IPQCInspectionResponse])
def list_inspections(
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(IPQCInspection)
    if status:
        query = query.filter(IPQCInspection.status == status)
    return query.order_by(IPQCInspection.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()


@router.post("/inspections", response_model=IPQCInspectionResponse, status_code=status.HTTP_201_CREATED)
def create_inspection(
    data: IPQCInspectionCreate,
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    existing = db.query(IPQCInspection).filter(IPQCInspection.inspection_no == data.inspection_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="So phieu kiem tra da ton tai")
    obj = IPQCInspection(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/inspections/{inspection_id}", response_model=IPQCInspectionResponse)
def get_inspection(inspection_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(IPQCInspection).filter(IPQCInspection.id == inspection_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu kiem tra")
    return obj


@router.put("/inspections/{inspection_id}/status")
def update_inspection_status(
    inspection_id: int,
    s: str = Query(..., alias="status", pattern="^(pending|pass|fail)$"),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    obj = db.query(IPQCInspection).filter(IPQCInspection.id == inspection_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu kiem tra")
    obj.status = s
    db.commit()
    return {"message": "Cap nhat trang thai thanh cong", "status": s}


@router.post("/inspections/{inspection_id}/results", response_model=IPQCResultResponse, status_code=status.HTTP_201_CREATED)
def add_result(
    inspection_id: int,
    data: IPQCResultCreate,
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    inspection = db.query(IPQCInspection).filter(IPQCInspection.id == inspection_id).first()
    if not inspection:
        raise HTTPException(status_code=404, detail="Khong tim thay phieu kiem tra")
    obj = IPQCResult(inspection_id=inspection_id, **data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/results/{result_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(result_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(IPQCResult).filter(IPQCResult.id == result_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay ket qua")
    db.delete(obj)
    db.commit()
