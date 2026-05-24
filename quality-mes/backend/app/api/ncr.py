from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database import get_db
from app.models.ncr import NCR, CAPA
from app.schemas.ncr import NCRCreate, NCRResponse, CAPACreate, CAPAResponse

router = APIRouter(prefix="/api/ncr", tags=["NCR"])


@router.get("/", response_model=list[NCRResponse])
def list_ncrs(
    status: str | None = Query(None),
    severity: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(NCR)
    if status:
        query = query.filter(NCR.status == status)
    if severity:
        query = query.filter(NCR.severity == severity)
    return query.order_by(NCR.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()


@router.post("/", response_model=NCRResponse, status_code=status.HTTP_201_CREATED)
def create_ncr(data: NCRCreate, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    existing = db.query(NCR).filter(NCR.ncr_no == data.ncr_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="So NCR da ton tai")
    obj = NCR(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{ncr_id}", response_model=NCRResponse)
def get_ncr(ncr_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(NCR).filter(NCR.id == ncr_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay NCR")
    return obj


@router.put("/{ncr_id}/status")
def update_ncr_status(
    ncr_id: int,
    s: str = Query(..., alias="status", pattern="^(open|investigating|resolved|closed)$"),
    resolution: str | None = Query(None),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    obj = db.query(NCR).filter(NCR.id == ncr_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay NCR")
    obj.status = s
    if resolution:
        obj.resolution = resolution
    db.commit()
    return {"message": "Cap nhat trang thai thanh cong", "status": s}


@router.put("/{ncr_id}", response_model=NCRResponse)
def update_ncr(ncr_id: int, data: NCRCreate, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(NCR).filter(NCR.id == ncr_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay NCR")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{ncr_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ncr(ncr_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(NCR).filter(NCR.id == ncr_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay NCR")
    db.delete(obj)
    db.commit()


# ---- CAPAs under NCR ----
@router.post("/{ncr_id}/capas", response_model=CAPAResponse, status_code=status.HTTP_201_CREATED)
def create_capa(ncr_id: int, data: CAPACreate, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    ncr = db.query(NCR).filter(NCR.id == ncr_id).first()
    if not ncr:
        raise HTTPException(status_code=404, detail="Khong tim thay NCR")
    existing = db.query(CAPA).filter(CAPA.capa_no == data.capa_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="So CAPA da ton tai")
    obj = CAPA(ncr_id=ncr_id, **data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/capas/{capa_id}", response_model=CAPAResponse)
def update_capa(capa_id: int, data: CAPACreate, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(CAPA).filter(CAPA.id == capa_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay CAPA")
    for key, value in data.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


@router.put("/capas/{capa_id}/status")
def update_capa_status(
    capa_id: int,
    s: str = Query(..., alias="status", pattern="^(open|in_progress|completed|verified)$"),
    effectiveness: str | None = Query(None),
    completed_date: str | None = Query(None),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    obj = db.query(CAPA).filter(CAPA.id == capa_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay CAPA")
    obj.status = s
    if effectiveness:
        obj.effectiveness = effectiveness
    if completed_date:
        from datetime import datetime
        obj.completed_date = datetime.fromisoformat(completed_date)
    db.commit()
    return {"message": "Cap nhat CAPA thanh cong", "status": s}


@router.delete("/capas/{capa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_capa(capa_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    obj = db.query(CAPA).filter(CAPA.id == capa_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Khong tim thay CAPA")
    db.delete(obj)
    db.commit()
