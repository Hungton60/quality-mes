from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import os

from app.api import auth, iqc, oqc, ipqc, spc, ncr, users, equipment, common, export
from app.core.database import init_db

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

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend", "dist")


@app.on_event("startup")
def on_startup():
    init_db()


app.mount("/assets", StaticFiles(directory=os.path.join(FRONTEND_DIR, "assets")), name="assets")


@app.get("/{full_path:path}")
async def serve_spa(full_path: str, request: Request):
    if full_path.startswith("api/"):
        return HTMLResponse(status_code=404)
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse(content="<h1>Frontend not built. Run: cd frontend && npm run build</h1>", status_code=404)
