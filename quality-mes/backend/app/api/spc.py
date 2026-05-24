from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database import get_db
from app.models.iqc import IQCInspection, IQCResult
from app.models.oqc import OQCInspection, OQCResult
from app.models.ipqc import IPQCInspection, IPQCResult

router = APIRouter(prefix="/api/spc", tags=["SPC"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    iqc_total = db.query(func.count(IQCInspection.id)).scalar() or 0
    iqc_pass = db.query(func.count(IQCInspection.id)).filter(IQCInspection.status == "pass").scalar() or 0
    iqc_fail = db.query(func.count(IQCInspection.id)).filter(IQCInspection.status == "fail").scalar() or 0

    oqc_total = db.query(func.count(OQCInspection.id)).scalar() or 0
    oqc_pass = db.query(func.count(OQCInspection.id)).filter(OQCInspection.status == "pass").scalar() or 0
    oqc_fail = db.query(func.count(OQCInspection.id)).filter(OQCInspection.status == "fail").scalar() or 0

    ipqc_total = db.query(func.count(IPQCInspection.id)).scalar() or 0
    ipqc_pass = db.query(func.count(IPQCInspection.id)).filter(IPQCInspection.status == "pass").scalar() or 0
    ipqc_fail = db.query(func.count(IPQCInspection.id)).filter(IPQCInspection.status == "fail").scalar() or 0

    return {
        "iqc": {"total": iqc_total, "pass": iqc_pass, "fail": iqc_fail},
        "oqc": {"total": oqc_total, "pass": oqc_pass, "fail": oqc_fail},
        "ipqc": {"total": ipqc_total, "pass": ipqc_pass, "fail": ipqc_fail},
    }


@router.get("/pareto/iqc")
def iqc_pareto(db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    results = (
        db.query(IQCResult.item_name, func.count(IQCResult.id).label("count"))
        .filter(IQCResult.result == "fail")
        .group_by(IQCResult.item_name)
        .order_by(func.count(IQCResult.id).desc())
        .limit(10)
        .all()
    )
    return [{"item_name": r.item_name, "count": r.count} for r in results]


@router.get("/pareto/oqc")
def oqc_pareto(db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    results = (
        db.query(OQCResult.item_name, func.count(OQCResult.id).label("count"))
        .filter(OQCResult.result == "fail")
        .group_by(OQCResult.item_name)
        .order_by(func.count(OQCResult.id).desc())
        .limit(10)
        .all()
    )
    return [{"item_name": r.item_name, "count": r.count} for r in results]


@router.get("/results/{module}")
def get_results(
    module: str,
    item_name: str | None = Query(None),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    if module not in ("iqc", "oqc", "ipqc"):
        return []

    model_map = {"iqc": IQCResult, "oqc": OQCResult, "ipqc": IPQCResult}
    model = model_map[module]

    query = db.query(model)
    if item_name:
        query = query.filter(model.item_name == item_name)

    rows = query.order_by(model.created_at.desc()).limit(limit).all()
    return [
        {
            "item_name": r.item_name,
            "measured_value": r.measured_value,
            "standard_min": r.standard_min,
            "standard_max": r.standard_max,
            "result": r.result,
            "created_at": str(r.created_at),
        }
        for r in rows
    ]
