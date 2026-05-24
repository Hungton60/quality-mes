from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database import get_db
from app.models.equipment import Equipment

router = APIRouter(prefix="/api/equipment", tags=["Equipment"])


@router.get("/")
def list_equipment(
    search: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(Equipment)
    if search:
        query = query.filter((Equipment.name.contains(search)) | (Equipment.code.contains(search)))
    if status:
        query = query.filter(Equipment.status == status)
    items = query.order_by(Equipment.name).all()

    today = date.today()
    result = []
    for eq in items:
        d = {
            "id": eq.id, "code": eq.code, "name": eq.name, "type": eq.type,
            "serial_no": eq.serial_no, "location": eq.location,
            "calibration_interval_days": eq.calibration_interval_days,
            "last_calibration_date": str(eq.last_calibration_date) if eq.last_calibration_date else None,
            "next_calibration_date": str(eq.next_calibration_date) if eq.next_calibration_date else None,
            "status": eq.status, "notes": eq.notes, "created_at": str(eq.created_at),
        }
        if eq.next_calibration_date:
            days_left = (eq.next_calibration_date - today).days
            d["days_until_calibration"] = days_left
            d["calibration_overdue"] = days_left < 0
        else:
            d["days_until_calibration"] = None
            d["calibration_overdue"] = False
        result.append(d)
    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_equipment(data: dict, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    existing = db.query(Equipment).filter(Equipment.code == data["code"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ma thiet bi da ton tai")
    eq = Equipment(
        code=data["code"],
        name=data["name"],
        type=data.get("type", "measurement"),
        serial_no=data.get("serial_no"),
        location=data.get("location"),
        calibration_interval_days=data.get("calibration_interval_days", 365),
        last_calibration_date=date.fromisoformat(data["last_calibration_date"]) if data.get("last_calibration_date") else None,
        next_calibration_date=date.fromisoformat(data["next_calibration_date"]) if data.get("next_calibration_date") else None,
        notes=data.get("notes"),
    )
    if eq.last_calibration_date and not eq.next_calibration_date:
        eq.next_calibration_date = eq.last_calibration_date + timedelta(days=eq.calibration_interval_days)
    db.add(eq)
    db.commit()
    db.refresh(eq)
    _log_activity(db, _token, "create", "equipment", f"Them thiet bi {eq.code} - {eq.name}")
    return {"id": eq.id, "code": eq.code, "name": eq.name, "status": eq.status}


@router.put("/{eq_id}/calibrate")
def calibrate(
    eq_id: int,
    calibration_date: str = Query(...),
    next_date: str | None = Query(None),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    eq = db.query(Equipment).filter(Equipment.id == eq_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Khong tim thay thiet bi")
    eq.last_calibration_date = date.fromisoformat(calibration_date)
    if next_date:
        eq.next_calibration_date = date.fromisoformat(next_date)
    else:
        eq.next_calibration_date = eq.last_calibration_date + timedelta(days=eq.calibration_interval_days)
    eq.status = "active"
    db.commit()
    _log_activity(db, _token, "calibrate", "equipment", f"Hieu chuan thiet bi {eq.code}")
    return {"message": "Hieu chuan thanh cong"}


@router.delete("/{eq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipment(eq_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    eq = db.query(Equipment).filter(Equipment.id == eq_id).first()
    if not eq:
        raise HTTPException(status_code=404, detail="Khong tim thay thiet bi")
    db.delete(eq)
    db.commit()


def _log_activity(db: Session, token: dict, action: str, module: str, description: str):
    from app.models.equipment import ActivityLog
    log = ActivityLog(
        user_id=int(token.get("sub", 0)),
        username=token.get("role", "unknown"),
        action=action,
        module=module,
        description=description,
    )
    db.add(log)
    db.commit()
