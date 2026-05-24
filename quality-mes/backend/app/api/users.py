from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.auth.security import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(
    role: str | None = Query(None),
    db: Session = Depends(get_db),
    token: dict = Depends(get_current_user),
):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Chi admin moi co quyen")
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.order_by(User.created_at.desc()).all()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    token: dict = Depends(get_current_user),
):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Chi admin moi co quyen")

    from app.auth.security import hash_password

    existing = db.query(User).filter((User.username == data.username) | (User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ten dang nhap hoac email da ton tai")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    role: str | None = Query(None),
    is_active: bool | None = Query(None),
    db: Session = Depends(get_db),
    token: dict = Depends(get_current_user),
):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Chi admin moi co quyen")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Khong tim thay nguoi dung")

    if role:
        if role not in ("admin", "qc_manager", "inspector", "operator"):
            raise HTTPException(status_code=400, detail="Vai tro khong hop le")
        user.role = role
    if is_active is not None:
        user.is_active = is_active

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(get_current_user),
):
    if token.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Chi admin moi co quyen")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Khong tim thay nguoi dung")

    db.delete(user)
    db.commit()
