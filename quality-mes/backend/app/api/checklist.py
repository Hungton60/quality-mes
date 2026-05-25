from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database import get_db
from app.models.checklist import ChecklistTemplate

router = APIRouter(prefix="/api/checklists", tags=["Checklists"])


@router.get("/")
def list_templates(
    module: str | None = Query(None),
    db: Session = Depends(get_db),
    _token: dict = Depends(get_current_user),
):
    query = db.query(ChecklistTemplate)
    if module:
        query = query.filter(ChecklistTemplate.module == module)
    templates = query.order_by(ChecklistTemplate.name).all()
    return [
        {
            "id": t.id, "code": t.code, "name": t.name, "module": t.module,
            "items": t.items, "created_at": str(t.created_at),
        }
        for t in templates
    ]


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_template(data: dict, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    existing = db.query(ChecklistTemplate).filter(ChecklistTemplate.code == data["code"]).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ma checklist da ton tai")
    if data["module"] not in ("iqc", "oqc", "ipqc"):
        raise HTTPException(status_code=400, detail="Module khong hop le")
    items = data.get("items", [])
    if isinstance(items, str):
        import json
        items = json.loads(items)
    t = ChecklistTemplate(code=data["code"], name=data["name"], module=data["module"], items=items)
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"id": t.id, "code": t.code, "name": t.name, "module": t.module, "items": t.items}


@router.put("/{template_id}")
def update_template(template_id: int, data: dict, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    t = db.query(ChecklistTemplate).filter(ChecklistTemplate.id == template_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Khong tim thay checklist")
    if "name" in data:
        t.name = data["name"]
    items = data.get("items")
    if items is not None:
        if isinstance(items, str):
            import json
            items = json.loads(items)
        t.items = items
    db.commit()
    return {"message": "Cap nhat thanh cong"}


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: int, db: Session = Depends(get_db), _token: dict = Depends(get_current_user)):
    t = db.query(ChecklistTemplate).filter(ChecklistTemplate.id == template_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Khong tim thay checklist")
    db.delete(t)
    db.commit()
