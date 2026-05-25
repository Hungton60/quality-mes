from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os

from app.api import auth, iqc, oqc, ipqc, spc, ncr, users, equipment, common, export, checklist
from app.core.database import init_db, SessionLocal

app = FastAPI(title="Quality MES API", version="1.0.0", docs_url="/api/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(iqc.router)
app.include_router(oqc.router)
app.include_router(ipqc.router)
app.include_router(spc.router)
app.include_router(ncr.router)
app.include_router(users.router)
app.include_router(equipment.router)
app.include_router(common.router)
app.include_router(export.router)
app.include_router(checklist.router)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend", "dist")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")

# Try frontend/dist first, fall back to backend/static
for fd in [FRONTEND_DIR, STATIC_DIR]:
    if os.path.isdir(fd) and os.path.exists(os.path.join(fd, "index.html")):
        FRONTEND_DIR = fd
        break


@app.on_event("startup")
def on_startup():
    init_db()
    try:
        from app.models.user import User
        from app.auth.security import hash_password
        db = SessionLocal()
        try:
            if db.query(User).count() == 0:
                db.add_all([
                    User(username="admin", email="admin@may.com", hashed_password=hash_password("Admin123"), full_name="Quan ly", role="admin"),
                    User(username="qc_manager", email="qc@may.com", hashed_password=hash_password("Qc123456"), full_name="Truong QC", role="qc_manager"),
                    User(username="inspector1", email="insp1@may.com", hashed_password=hash_password("Insp123456"), full_name="Kiem tra vien A", role="inspector"),
                ])
                db.commit()
                print("Default users created")
        finally:
            db.close()
    except Exception as e:
        print(f"Startup warning: {e}")


@app.get("/api/health")
def health():
    import glob as g
    p = PROJECT_ROOT
    f = FRONTEND_DIR
    return {
        "status": "ok",
        "project_root": p,
        "frontend_dir": f,
        "index_exists": os.path.exists(os.path.join(f, "index.html")),
        "dist_contents": os.listdir(f) if os.path.isdir(f) else "NOT FOUND",
    }


assets_dir = os.path.join(FRONTEND_DIR, "assets")
if os.path.isdir(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    if full_path.startswith("api/"):
        return HTMLResponse(status_code=404)
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse(content="<h1>Frontend not built.</h1>", status_code=404)
