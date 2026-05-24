from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    from app.models.user import User  # noqa: F401
    from app.models.iqc import Supplier, Material, IQCInspection, IQCResult  # noqa: F401
    from app.models.oqc import Product, OQCInspection, OQCResult  # noqa: F401
    from app.models.ipqc import IPQCInspection, IPQCResult  # noqa: F401
    from app.models.ncr import NCR, CAPA  # noqa: F401
    from app.models.equipment import Equipment, ActivityLog  # noqa: F401
    Base.metadata.create_all(bind=engine)
