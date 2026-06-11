"""
db.py — Lớp lưu trữ dữ liệu Quality MES
Backend: Google Sheets (lưu vĩnh viễn) + JSON local (fallback)

Cách hoạt động:
- Mỗi danh sách (iqc_list, users_list...) = 1 sheet tab trong Google Spreadsheet
- Đọc/ghi qua Google Sheets API bằng Service Account
- Nếu chưa cấu hình Google Sheets → fallback về JSON file /tmp
"""

import json, os, time
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

# ── Fallback: JSON local ───────────────────────────────────
DATA_DIR = Path(os.environ.get("QUALITY_MES_DATA_DIR", "/tmp/quality_mes_data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Tên các sheet tab trong Google Spreadsheet ────────────
SHEET_KEYS = ["users_list","iqc_list","ipqc_list","oqc_list",
              "ncr_list","capa_list","dev_list","log_list"]

DEFAULTS = {
    "users_list": [
        {"Tài khoản":"admin","Họ tên":"Quản lý","Mật khẩu":"admin123",
         "Phân quyền":"Quản lý","Trạng thái":"Hoạt động"},
    ],
    "iqc_list": [], "ipqc_list": [], "oqc_list": [],
    "ncr_list": [], "capa_list": [], "dev_list": [], "log_list": [],
}

# ══════════════════════════════════════════════════════════
# GOOGLE SHEETS CLIENT
# ══════════════════════════════════════════════════════════
def _get_gspread_client():
    """
    Kết nối Google Sheets qua Service Account credentials.
    Credentials lưu trong st.secrets["gcp_service_account"] hoặc
    biến môi trường GOOGLE_CREDENTIALS (JSON string).
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials

        SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        # Thử đọc từ Streamlit secrets trước
        if hasattr(st, "secrets") and "gcp_service_account" in st.secrets:
            creds_dict = dict(st.secrets["gcp_service_account"])
        elif os.environ.get("GOOGLE_CREDENTIALS"):
            creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
        else:
            return None  # Chưa cấu hình → dùng JSON local

        creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        return gspread.authorize(creds)
    except Exception as e:
        return None


def _get_spreadsheet():
    """Lấy Google Spreadsheet object theo SPREADSHEET_ID trong secrets."""
    gc = _get_gspread_client()
    if gc is None:
        return None
    try:
        if hasattr(st, "secrets") and "spreadsheet_id" in st.secrets:
            sid = st.secrets["spreadsheet_id"]
        elif os.environ.get("SPREADSHEET_ID"):
            sid = os.environ["SPREADSHEET_ID"]
        else:
            return None
        return gc.open_by_key(sid)
    except Exception:
        return None


def _ensure_sheet(spreadsheet, sheet_name: str):
    """Tạo sheet tab nếu chưa có."""
    try:
        return spreadsheet.worksheet(sheet_name)
    except Exception:
        return spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=30)


# ══════════════════════════════════════════════════════════
# GOOGLE SHEETS: ĐỌC / GHI
# ══════════════════════════════════════════════════════════
def _gs_load(sheet_name: str) -> list | None:
    """Đọc 1 sheet tab → list of dicts. Trả None nếu lỗi."""
    try:
        ss = _get_spreadsheet()
        if ss is None:
            return None
        ws = _ensure_sheet(ss, sheet_name)
        records = ws.get_all_records(default_blank="")
        if not records:
            return []
        # Chuyển list dicts chuỗi → parse JSON fields (Files là list)
        result = []
        for rec in records:
            row = {}
            for k, v in rec.items():
                if isinstance(v, str) and v.startswith("["):
                    try:
                        row[k] = json.loads(v)
                    except Exception:
                        row[k] = v
                else:
                    row[k] = v
            result.append(row)
        return result
    except Exception:
        return None


def _gs_save(sheet_name: str, data: list) -> bool:
    """Ghi toàn bộ list of dicts vào 1 sheet tab. Trả True nếu thành công."""
    try:
        ss = _get_spreadsheet()
        if ss is None:
            return False
        ws = _ensure_sheet(ss, sheet_name)
        ws.clear()

        if not data:
            return True

        # Lấy tất cả keys từ tất cả rows (union)
        all_keys = list({k for row in data for k in row.keys()})
        # Loại Người tạo ra khỏi header hiển thị không cần thiết — vẫn giữ trong data

        # Header row
        ws.append_row(all_keys, value_input_option="RAW")

        # Data rows — list fields → JSON string
        rows_to_write = []
        for row in data:
            r = []
            for k in all_keys:
                v = row.get(k, "")
                if isinstance(v, list):
                    v = json.dumps(v, ensure_ascii=False)
                r.append(str(v) if v is not None else "")
            rows_to_write.append(r)

        # Batch write để tránh rate limit
        if rows_to_write:
            ws.append_rows(rows_to_write, value_input_option="RAW")
        return True
    except Exception as e:
        return False


# ══════════════════════════════════════════════════════════
# PUBLIC API — dùng trong QualityMES_FINAL.py
# ══════════════════════════════════════════════════════════
def _json_path(key: str) -> Path:
    return DATA_DIR / f"{key}.json"


def load_data(key: str) -> list:
    """Đọc dữ liệu: thử Google Sheets trước, fallback JSON local."""
    # 1. Thử Google Sheets
    gs_data = _gs_load(key)
    if gs_data is not None:
        # Cache vào JSON local làm backup
        _json_path(key).write_text(
            json.dumps(gs_data, ensure_ascii=False, indent=2), encoding="utf-8")
        return gs_data

    # 2. Fallback: JSON local
    path = _json_path(key)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass

    # 3. Default
    return list(DEFAULTS.get(key, []))


def save_data(key: str, data: list) -> None:
    """Ghi dữ liệu: luôn ghi JSON local, thêm Google Sheets nếu đã cấu hình."""
    # Luôn ghi JSON local (backup tức thì)
    _json_path(key).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    # Ghi Google Sheets (async-ish, lỗi sẽ bị bỏ qua)
    _gs_save(key, data)


def save_all(session_state) -> None:
    """Lưu tất cả danh sách từ session_state."""
    for key in SHEET_KEYS:
        if key in session_state:
            save_data(key, session_state[key])


def backup_json(session_state) -> bytes:
    """Tạo file backup JSON tổng hợp."""
    backup = {key: list(session_state.get(key, [])) for key in SHEET_KEYS}
    backup["_exported_at"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return json.dumps(backup, ensure_ascii=False, indent=2).encode("utf-8")


def restore_json(uploaded_bytes: bytes, session_state) -> tuple:
    """Restore từ file backup JSON → cả local lẫn Google Sheets."""
    try:
        data = json.loads(uploaded_bytes.decode("utf-8"))
        restored = []
        for key in SHEET_KEYS:
            if key in data:
                session_state[key] = data[key]
                save_data(key, data[key])
                restored.append(key)
        return True, f"Đã khôi phục: {', '.join(restored)}"
    except Exception as e:
        return False, f"Lỗi: {e}"


def gs_status() -> dict:
    """Kiểm tra trạng thái kết nối Google Sheets."""
    ss = _get_spreadsheet()
    if ss is None:
        return {"connected": False, "message": "Chưa cấu hình Google Sheets"}
    try:
        title = ss.title
        return {"connected": True, "message": f"Đã kết nối: {title}"}
    except Exception as e:
        return {"connected": False, "message": f"Lỗi: {e}"}
