import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
from collections import Counter
from db import load_data, save_data, save_all, backup_json, restore_json, gs_status

# ── Logo công ty (base64 embedded) ──
LOGO_B64 = "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"
LOGO_SRC = f"data:image/png;base64,{LOGO_B64}"

# ══════════════════════════════════════════════════════════
# CONFIG & CSS
# ══════════════════════════════════════════════════════════
st.set_page_config(page_title="Quality MES", layout="wide", initial_sidebar_state="expanded",
                   page_icon="🏭")
st.markdown("""
<style>
  /* ── Reset & Base ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; }

  /* ── Fix header clipping ── */
  .block-container {
    padding-top: 2.5rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    max-width: 100% !important;
  }

  /* ── Page title style ── */
  h2 { 
    font-size: 1.55rem !important; 
    font-weight: 700 !important; 
    color: #1e293b !important;
    letter-spacing: -0.02em;
    padding-top: 0.1rem !important;
    margin-bottom: 0.8rem !important;
    border-left: 4px solid #0d9488;
    padding-left: 12px !important;
  }
  h3 { color: #1e293b !important; font-weight: 600 !important; }

  /* ── Sidebar ── */
  section[data-testid="stSidebar"] {
    background: #1e293b !important;
    border-right: 1px solid #334155;
  }
  section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
  section[data-testid="stSidebar"] .stRadio label { 
    font-size: 13px !important; 
    padding: 6px 8px;
    border-radius: 6px;
    transition: background 0.15s;
  }
  section[data-testid="stSidebar"] .stRadio label:hover { background: #334155 !important; }
  section[data-testid="stSidebar"] hr { border-color: #334155 !important; }
  section[data-testid="stSidebar"] .stCaption { color: #94a3b8 !important; }
  section[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }

  /* ── Metric cards ── */
  .mc {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
    margin-bottom: 12px;
    transition: box-shadow 0.2s;
  }
  .mc:hover { box-shadow: 0 4px 12px rgba(0,0,0,.08); }
  .mc-label { font-size: 11px; color: #64748b; margin: 0; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; }
  .mc-value { font-size: 28px; font-weight: 800; margin: 6px 0 0; line-height: 1; letter-spacing: -0.02em; }

  /* ── Feature/section cards ── */
  .fc {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 20px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
    margin-bottom: 12px;
    transition: all 0.2s;
  }
  .fc:hover { box-shadow: 0 4px 16px rgba(0,0,0,.09); transform: translateY(-1px); }
  .fc-icon {
    width: 52px; height: 52px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 22px; flex-shrink: 0;
  }
  .fc-title { font-weight: 700; font-size: 14px; color: #1e293b; margin-bottom: 3px; }
  .fc-desc { font-size: 12px; color: #64748b; margin-bottom: 4px; }
  .fc-sub { font-size: 12px; font-weight: 600; color: #475569; }

  /* ── SPC summary cards ── */
  .spc-card {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,.05);
  }
  .spc-title { font-weight: 700; font-size: 16px; color: #1e293b; margin-bottom: 12px; }
  .spc-row { display: flex; gap: 28px; flex-wrap: wrap; }
  .spc-stat-label { font-size: 11px; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
  .spc-stat-val { font-size: 22px; font-weight: 800; margin-top: 3px; letter-spacing: -0.02em; }
  .badge { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; letter-spacing: 0.02em; }
  .badge-pass { background: #dcfce7; color: #166534; }
  .badge-fail { background: #fee2e2; color: #991b1b; }

  /* ── Status badges ── */
  .tt-pass { background:#dcfce7; color:#166534; font-weight:700; padding:4px 12px; border-radius:20px; font-size:12px; white-space:nowrap; }
  .tt-fail { background:#fee2e2; color:#991b1b; font-weight:700; padding:4px 12px; border-radius:20px; font-size:12px; white-space:nowrap; }
  .tt-warn { background:#fef9c3; color:#854d0e; font-weight:700; padding:4px 12px; border-radius:20px; font-size:12px; white-space:nowrap; }
  .tt-ok   { background:#d1fae5; color:#065f46; font-weight:700; padding:4px 12px; border-radius:20px; font-size:12px; white-space:nowrap; }

  /* ── Buttons ── */
  .stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.15s !important;
  }
  .stButton > button[kind="primary"] {
    background: #0d9488 !important;
    border-color: #0d9488 !important;
  }
  .stButton > button[kind="primary"]:hover { background: #0f766e !important; }
  .stDownloadButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    color: #475569 !important;
  }
  .stDownloadButton > button:hover { background: #f1f5f9 !important; border-color: #cbd5e1 !important; }

  /* ── Expanders ── */
  .streamlit-expanderHeader {
    background: #f8fafc !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    color: #1e293b !important;
  }
  .streamlit-expanderContent {
    border: 1px solid #e2e8f0 !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
    background: #fff !important;
  }

  /* ── Forms & Inputs ── */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea,
  .stSelectbox > div > div {
    border-radius: 8px !important;
    border-color: #e2e8f0 !important;
    font-size: 13px !important;
  }
  .stTextInput > label, .stTextArea > label, .stSelectbox > label,
  .stFileUploader > label, .stDateInput > label, .stTimeInput > label {
    font-size: 12px !important;
    font-weight: 600 !important;
    color: #475569 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
  }

  /* ── DataFrames ── */
  div[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0 !important;
    border-radius: 10px !important;
    overflow: hidden;
  }
  div[data-testid="stDataFrame"] table { font-size: 13px !important; font-family: 'Inter', sans-serif !important; }
  div[data-testid="stDataFrame"] thead th {
    background: #f8fafc !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    color: #64748b !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    white-space: nowrap !important;
    padding: 10px 12px !important;
    border-bottom: 2px solid #e2e8f0 !important;
  }
  div[data-testid="stDataFrame"] tbody td {
    padding: 9px 12px !important;
    color: #334155 !important;
    border-bottom: 1px solid #f1f5f9 !important;
  }
  div[data-testid="stDataFrame"] tbody tr:hover td { background: #f8fafc !important; }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 2px solid #e2e8f0; }
  .stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    color: #64748b !important;
    padding: 10px 18px !important;
  }
  .stTabs [aria-selected="true"] {
    background: #fff !important;
    color: #0d9488 !important;
    border-bottom: 2px solid #0d9488 !important;
  }

  /* ── Action row (per-row edit/delete) ── */
  .action-row {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid #f1f5f9;
    background: #fff;
    margin-bottom: 4px;
    gap: 8px;
    transition: background 0.15s;
  }
  .action-row:hover { background: #f8fafc; border-color: #e2e8f0; }
  .action-row-id { font-weight: 700; font-size: 13px; color: #1e293b; min-width: 90px; }
  .action-row-info { font-size: 12px; color: #64748b; flex: 1; }

  /* ── Search bar ── */
  .stTextInput[data-testid="search"] > div > div > input {
    background: #f8fafc !important;
    border-color: #e2e8f0 !important;
    font-size: 13px !important;
  }

  /* ── Dividers ── */
  hr { border-color: #f1f5f9 !important; margin: 8px 0 !important; }

  /* ── Popover ── */
  div[data-testid="stPopover"] > div {
    border-radius: 10px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.12) !important;
  }
  /* ── Login screen ── */
  .login-wrap {
    max-width: 420px;
    margin: 6vh auto 0 auto;
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 44px 40px 36px;
    box-shadow: 0 8px 32px rgba(0,0,0,.10);
  }
  .login-logo { text-align: center; margin-bottom: 8px; font-size: 36px; }
  .login-title { text-align: center; font-size: 22px; font-weight: 800;
    color: #1e293b; margin-bottom: 4px; }
  .login-sub { text-align: center; font-size: 13px; color: #64748b;
    margin-bottom: 28px; }
  .login-err { background: #fff1f2; border: 1px solid #fda4af;
    color: #be123c; border-radius: 8px; padding: 10px 14px;
    font-size: 13px; font-weight: 600; margin-bottom: 16px; text-align:center; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════
def _init(k, v):
    """Load từ DB nếu có, không thì dùng default v"""
    if k not in st.session_state:
        if k in ("current_user","spc_df"):
            st.session_state[k] = v
        else:
            st.session_state[k] = load_data(k) or v

_init("current_user", None)          # None = chưa đăng nhập
_init("login_error", "")
_init("users_list",[
    {"Tài khoản":"admin","Họ tên":"Quản lý","Mật khẩu":"admin123","Phân quyền":"Quản lý","Trạng thái":"Hoạt động"},
    {"Tài khoản":"qc_trang","Họ tên":"Trưởng QC","Mật khẩu":"trang123","Phân quyền":"Trưởng QC","Trạng thái":"Hoạt động"},
    {"Tài khoản":"ktv1","Họ tên":"Kiểm tra viên 1","Mật khẩu":"123","Phân quyền":"Kiểm tra viên","Trạng thái":"Hoạt động"},
    {"Tài khoản":"ktv2","Họ tên":"Kiểm tra viên 2","Mật khẩu":"123","Phân quyền":"Kiểm tra viên","Trạng thái":"Hoạt động"},
    {"Tài khoản":"ktv3","Họ tên":"Kiểm tra viên 3","Mật khẩu":"123","Phân quyền":"Kiểm tra viên","Trạng thái":"Hoạt động"},
])
_init("iqc_list",[
    {"Số phiếu":"IQC-001","Mã dự án":"DA-68","Khách hàng":"68 Residence","Tên vật tư":"Nhôm thanh al","Nhà cung cấp":"An Lập","Lô":"LOT-01","SL mẫu":"5","Thời gian kiểm":"05-06-2026 08:00","Người kiểm":"Kiểm tra viên 1","Files":[],"Trạng thái":"Đạt (Pass)","Ghi chú":"-","Người tạo":"ktv1"},
    {"Số phiếu":"IQC-002","Mã dự án":"DA-AURORA","Khách hàng":"Siber Facade","Tên vật tư":"Kính hộp glass","Nhà cung cấp":"csg","Lô":"LOT-02","SL mẫu":"10","Thời gian kiểm":"05-06-2026 10:15","Người kiểm":"Kiểm tra viên 2","Files":["GLASS_CHECKLIST.xlsx"],"Trạng thái":"Đạt (Pass)","Ghi chú":"-","Người tạo":"ktv2"},
    {"Số phiếu":"IQC-003","Mã dự án":"DA-68","Khách hàng":"68 Residence","Tên vật tư":"Gioăng cao su","Nhà cung cấp":"Lixil","Lô":"LOT-03","SL mẫu":"5","Thời gian kiểm":"06-06-2026 14:20","Người kiểm":"Kiểm tra viên 1","Files":["ANH_KIEM_TRA.jpg"],"Trạng thái":"Không đạt (Failed)","Ghi chú":"Lỗi kích thước dày","Người tạo":"ktv1"},
])
_init("ipqc_list",[
    {"Số phiếu":"IPQC-001","Mã dự án":"DA-68","Khách hàng":"68 Residence","Tên công đoạn":"Gia công cắt nhôm","Lô":"LOT-A","SL mẫu":"5","Thời gian kiểm":"09-06-2026 09:00","Người kiểm":"Kiểm tra viên 2","Files":["PROCESS_CUTTING.pdf"],"Trạng thái":"Đạt (Pass)","Ghi chú":"-","Người tạo":"ktv2"},
])
_init("oqc_list",[
    {"Số phiếu":"OQC-001","Mã dự án":"DA-68","Khách hàng":"68 Residence","Mã/Tên SP":"Cửa sổ mở hất lật Aluminium","Lô":"LOT-OQC-01","SL mẫu":"8","Thời gian kiểm":"09-06-2026 13:45","Người kiểm":"Kiểm tra viên 3","Files":[],"Trạng thái":"Đạt (Pass)","Ghi chú":"-","Người tạo":"ktv3"},
])
_init("ncr_list",[
    {"Số NCR":"NCR-001","Mã dự án":"DA-68","Khách hàng":"68 Residence","Tên vật tư/SP":"Kính bị bọt khí","Lô":"LOT-01","SL phát hiện":"2 vách","Thời gian":"05-06-2026 10:00","Người phát hiện":"Kiểm tra viên 1","Người lập":"Quản lý","Mức độ":"Vừa","Trạng thái":"Đang điều tra","Files":[],"Ghi chú":"-","Người tạo":"admin"},
])
_init("capa_list",[
    {"Mã CAPA":"CAPA-001","Số NCR":"NCR-001","Nguyên nhân":"Áp suất bơm keo không đều","Khắc phục":"Cô lập vách kính lỗi","Phòng ngừa":"Bảo dưỡng định kỳ","Bộ phận":"Tổ kính","Thời hạn":"25-06-2026","Người lập":"Quản lý","Trạng thái CAPA":"Đang tiến hành","Files":[],"Ghi chú":"-","Người tạo":"admin"},
])
_init("dev_list",[
    {"Mã TB":"TB-001","Tên thiết bị":"Thước cặp Mitutoyo","Số serie":"MTY-500","Vị trí":"Xưởng cắt","Chu kỳ HC":"12 tháng","HC lần cuối":"15-01-2026","Hạn HC":"15-01-2027","Tình trạng":"Sử dụng tốt","Người lập":"Quản lý","Ghi chú":"-","Người tạo":"admin"},
])
_init("log_list",[
    {"Thời gian":"09-06-2026 11:30","Tài khoản":"admin","Phân hệ":"IQC","Hành động":"Tạo mới","Chi tiết":"Khởi tạo phiếu IQC-002"},
])
_init("spc_df", None)

# ══════════════════════════════════════════════════════════
# HÀM GHI LOG (định nghĩa sớm để dùng trong login)
# ══════════════════════════════════════════════════════════
def ghi_log_anon(action, detail):
    st.session_state.log_list.insert(0,{
        "Thời gian": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "Tài khoản": "system", "Phân hệ": "Auth",
        "Hành động": action, "Chi tiết": detail})
    save_data("log_list", st.session_state.log_list)

# ══════════════════════════════════════════════════════════
# LOGIN SCREEN — hiển thị nếu chưa đăng nhập
# ══════════════════════════════════════════════════════════
if st.session_state.current_user is None:
    # Ẩn sidebar khi chưa đăng nhập
    st.markdown("""<style>
        section[data-testid="stSidebar"]{display:none!important}
        .block-container{padding-top:0!important}
    </style>""", unsafe_allow_html=True)

    # Căn giữa form đăng nhập
    _, col_c, _ = st.columns([1, 1.4, 1])
    with col_c:
        st.markdown(f"""
        <div class="login-wrap">
          <div class="login-logo">
            <img src="{LOGO_SRC}" style="width:56px;height:auto;border-radius:8px"/>
          </div>
          <div class="login-title">QUALITY MES</div>
          <div class="login-sub">Hệ thống quản lý chất lượng sản xuất · v1.0</div>
        </div>
        """, unsafe_allow_html=True)

        # Hiện lỗi nếu có
        if st.session_state.login_error:
            st.markdown(
                f'<div class="login-err">⚠️ {st.session_state.login_error}</div>',
                unsafe_allow_html=True)

        with st.form("frm_login", clear_on_submit=False):
            username = st.text_input("Tài khoản", placeholder="Nhập tên tài khoản...")
            password = st.text_input("Mật khẩu", type="password",
                                     placeholder="Nhập mật khẩu...")
            submitted = st.form_submit_button("🔐 Đăng nhập",
                                              use_container_width=True, type="primary")
            if submitted:
                if not username or not password:
                    st.session_state.login_error = "Vui lòng điền đầy đủ tài khoản và mật khẩu."
                    st.rerun()
                else:
                    # Tìm user trong danh sách
                    matched = None
                    for u in st.session_state.users_list:
                        if (u["Tài khoản"].strip().lower() == username.strip().lower()
                                and u["Mật khẩu"] == password
                                and u.get("Trạng thái","Hoạt động") == "Hoạt động"):
                            matched = u
                            break
                    if matched:
                        st.session_state.current_user = {
                            "Tài khoản": matched["Tài khoản"],
                            "Họ tên":    matched["Họ tên"],
                            "Vai trò":   matched["Phân quyền"],
                        }
                        st.session_state.login_error = ""
                        ghi_log_anon("Đăng nhập", f"{matched['Họ tên']} đăng nhập thành công")
                        st.rerun()
                    else:
                        st.session_state.login_error = "Tài khoản hoặc mật khẩu không đúng."
                        st.rerun()
    st.stop()   # Không render gì thêm khi chưa login

# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════
cu = st.session_state.current_user

# Role badge color
role_colors = {"Quản lý":"#f59e0b","Trưởng QC":"#10b981","Kiểm tra viên":"#818cf8"}
role_bg = {"Quản lý":"#451a03","Trưởng QC":"#064e3b","Kiểm tra viên":"#1e1b4b"}
rc = role_colors.get(cu["Vai trò"],"#94a3b8")
rb = role_bg.get(cu["Vai trò"],"#1e293b")

st.sidebar.markdown(f"""
<div style="padding:16px 4px 18px 4px;border-bottom:1px solid #334155;margin-bottom:4px">
  <div style="display:flex;align-items:flex-end;gap:12px;margin-bottom:10px">
    <img src="{LOGO_SRC}" style="width:44px;height:auto;border-radius:6px;flex-shrink:0;margin-bottom:4px"/>
    <div>
      <div style="font-size:22px;font-weight:900;color:#f1f5f9;letter-spacing:0.03em;line-height:1;white-space:nowrap">
        QUALITY MES
      </div>
    </div>
  </div>
  <div style="font-size:10px;color:#64748b;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-top:2px;margin-bottom:10px">
    V1.0
  </div>
  <div style="font-size:11px;color:#94a3b8;text-transform:uppercase;letter-spacing:.08em;font-weight:600;margin-bottom:5px">Đang đăng nhập</div>
  <div style="font-size:15px;font-weight:700;color:#f1f5f9;margin-bottom:8px">👤 {cu['Họ tên']}</div>
  <span style="background:{rb};color:{rc};padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;border:1px solid {rc}33">{cu['Vai trò']}</span>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# ── Trạng thái lưu trữ ──
_gs = gs_status()
if _gs["connected"]:
    st.sidebar.markdown(
        f"<div style='font-size:11px;color:#4ade80;padding:4px 0'>🟢 Google Sheets: Đã kết nối</div>",
        unsafe_allow_html=True)
else:
    st.sidebar.markdown(
        f"<div style='font-size:11px;color:#f87171;padding:4px 0'>🔴 Lưu local (JSON)</div>",
        unsafe_allow_html=True)
st.sidebar.markdown("---")

MENU = ["📊 Bảng điều khiển","✅ Kiểm tra đầu vào (IQC)","🧪 Kiểm tra quá trình (IPQC)",
        "📦 Kiểm tra thành phẩm (OQC)","⚠️ NCR + CAPA","🔧 Thiết bị đo",
        "📊 Báo cáo (SPC)","📜 Nhật ký hoạt động","👤 Quản lý người dùng"]
page = st.sidebar.radio("DANH MỤC", MENU, index=0)

st.sidebar.markdown("---")
if st.sidebar.button("🚪 Đăng xuất", use_container_width=True):
    ghi_log_anon("Đăng xuất", f"{cu['Họ tên']} đăng xuất")
    st.session_state.current_user = None
    st.session_state.login_error  = ""
    st.rerun()

# ══════════════════════════════════════════════════════════
# TIỆN ÍCH CHUNG
# ══════════════════════════════════════════════════════════
def ghi_log(phane, action, detail):
    st.session_state.log_list.insert(0,{
        "Thời gian":datetime.now().strftime("%d-%m-%Y %H:%M"),
        "Tài khoản":cu["Tài khoản"],"Phân hệ":phane,"Hành động":action,"Chi tiết":detail})
    # Auto-save log
    save_data("log_list", st.session_state.log_list)

def persist(key: str):
    """Lưu ngay một key ra DB sau khi thay đổi"""
    save_data(key, st.session_state[key])

def co_quyen_sua(nguoi_tao, all_users=False):
    """
    all_users=False (mặc định): Admin/QC sửa tất cả, KTV chỉ sửa của mình
    all_users=True: mọi user đều được sửa/xóa (NCR, CAPA, Thiết bị đo)
    """
    if all_users: return True
    role = cu["Vai trò"]
    if role in ["Quản lý","Trưởng QC"]: return True
    return nguoi_tao == cu["Tài khoản"]

def unames():
    return [u["Họ tên"] for u in st.session_state.users_list]

def badge_tt(val):
    s = str(val)
    if "Pass" in s or "Đạt" in s:     cls = "tt-pass"
    elif "Failed" in s or "Không" in s: cls = "tt-fail"
    elif "Đang" in s:                   cls = "tt-warn"
    elif "Hoàn" in s or "Đóng" in s:   cls = "tt-ok"
    else: return f"<span>{val}</span>"
    return f'<span class="{cls}">{val}</span>'

def badge_tinhtrang(val):
    if val=="Sử dụng tốt":    cls="tt-pass"
    elif val=="Chờ hiệu chuẩn":cls="tt-warn"
    elif val=="Hỏng":          cls="tt-fail"
    else: return f"<span>{val}</span>"
    return f'<span class="{cls}">{val}</span>'

def fmt_files_list(files_list):
    """Hiển thị danh sách file names"""
    if not files_list: return "(Không có file)"
    return " · ".join(files_list)

def csv_download(lst, fname, key=None):
    # Tạo bản copy để export (thay Files list thành string)
    export = []
    for r in lst:
        row = dict(r)
        if "Files" in row:
            row["File đính kèm"] = fmt_files_list(row["Files"])
            del row["Files"]
        export.append(row)
    data = pd.DataFrame(export).to_csv(index=False).encode("utf-8-sig")
    kw = {"key":key} if key else {}
    st.download_button("📥 Xuất dữ liệu CSV", data=data, file_name=fname, mime="text/csv", **kw)

# ══════════════════════════════════════════════════════════
# WIDGET: BẢNG ĐẸP (st.dataframe) + HÀNG THAO TÁC SỬA/XÓA
# ══════════════════════════════════════════════════════════
def render_table_actions(data_list, id_field, phane, schema, edit_form_fn,
                          badge_col=None, badge_fn=None, search_fields=None, all_users=False):
    """
    Hiển thị:
    1. Ô tìm kiếm (search_fields: list tên field được tìm)
    2. Bảng st.dataframe đẹp
    3. Mỗi hàng: nút ✏️ Sửa (popover) + 🗑️ Xóa (có confirm)
    """
    if not data_list:
        st.info("Chưa có dữ liệu"); return

    # ── 1. THANH TÌM KIẾM ────────────────────────────────────────
    sf1, sf2 = st.columns([3, 1])
    search_val = sf1.text_input(
        "🔍 Tìm kiếm", placeholder="Nhập từ khóa để lọc...",
        key=f"search_{phane}", label_visibility="collapsed"
    )
    # Xác định các field được search (mặc định: tất cả text field trong schema)
    s_fields = search_fields or [fk for _, fk, _ in schema if fk != "Files"]
    sf2.caption(f"Tổng: **{len(data_list)}** bản ghi")

    # Lọc dữ liệu theo từ khóa
    if search_val.strip():
        kw = search_val.strip().lower()
        filtered_indices = [
            i for i, row in enumerate(data_list)
            if any(kw in str(row.get(fk,"")).lower() for fk in s_fields)
        ]
        if not filtered_indices:
            st.warning(f"Không tìm thấy kết quả cho: **{search_val}**")
            return
        working_list = [data_list[i] for i in filtered_indices]
        real_indices  = filtered_indices
        sf2.caption(f"Kết quả: **{len(filtered_indices)}** / {len(data_list)}")
    else:
        working_list = data_list
        real_indices  = list(range(len(data_list)))

    # ── 2. BẢNG HIỂN THỊ ─────────────────────────────────────────
    display_rows = []
    for row in working_list:
        r = {}
        for lbl, fk, _ in schema:
            val = row.get(fk, "-")
            if fk == "Files": val = fmt_files_list(val)
            r[lbl] = val
        display_rows.append(r)

    df = pd.DataFrame(display_rows)

    badge_label = None
    if badge_col:
        for lbl, fk, _ in schema:
            if fk == badge_col: badge_label = lbl; break

    # CSS style functions cho st.dataframe (không dùng HTML badge_fn ở đây)
    css_fn = c_tinhtrang if badge_fn == badge_tinhtrang else c_tt
    s = df.style.set_properties(**{
        "font-size":"13px","white-space":"nowrap","padding":"7px 10px",
    }).set_table_styles([
        {"selector":"thead th","props":[
            ("background","#f1f3f5"),("font-weight","700"),("font-size","12px"),
            ("color","#495057"),("border","1px solid #dee2e6"),
            ("padding","9px 10px"),("white-space","nowrap")]},
        {"selector":"tbody td","props":[("border","1px solid #f1f3f5")]},
        {"selector":"tbody tr:hover","props":[("background","#f8f9fa")]},
        {"selector":"table","props":[("border-collapse","collapse"),("width","100%")]},
    ])
    if badge_label and badge_label in df.columns:
        s = s.map(css_fn, subset=[badge_label])

    st.dataframe(s, use_container_width=True, hide_index=True)

    # ── 3. HÀNG THAO TÁC SỬA / XÓA (có confirm) ─────────────────
    st.markdown("---")
    for local_idx, (real_idx, row) in enumerate(zip(real_indices, working_list)):
        can = co_quyen_sua(row.get("Người tạo",""), all_users=all_users)
        rid = row.get(id_field, f"#{real_idx}")
        extra_fields = [(lbl,fk) for lbl,fk,_ in schema if fk not in (id_field,"Người tạo","Files")]
        extra = "  ·  ".join(str(row.get(fk,"-")) for _,fk in extra_fields[:3])

        c_id, c_info, c_edit, c_del = st.columns([1.2, 5.5, 0.9, 0.9])
        c_id.markdown(f"**{rid}**")
        c_info.caption(extra)

        if can:
            # Nút SỬA — popover form
            with c_edit.popover("✏️ Sửa"):
                edit_form_fn(real_idx, row)

            # Nút XÓA — popover confirm trước khi xóa
            with c_del.popover("🗑️ Xóa"):
                st.warning(f"Xác nhận xóa **{rid}**?")
                st.caption(extra)
                col_yes, col_no = st.columns(2)
                if col_yes.button("✅ Xác nhận", key=f"confirm_del_{phane}_{real_idx}", use_container_width=True):
                    data_list.pop(real_idx)
                    ghi_log(phane,"Xóa",f"Xóa {rid}")
                    st.rerun()
                col_no.button("❌ Hủy", key=f"cancel_del_{phane}_{real_idx}", use_container_width=True)
        else:
            c_edit.caption("🔒")
            c_del.caption("—")

# ══════════════════════════════════════════════════════════
# WIDGET: QUẢN LÝ FILE ĐÍNH KÈM (thêm/xóa từng file)
# ══════════════════════════════════════════════════════════
def file_manager_widget(files_list, key_prefix):
    """
    Hiển thị danh sách file hiện tại với nút xóa từng file,
    và uploader để thêm file mới.
    Trả về danh sách file names sau khi thay đổi.
    """
    result = list(files_list)  # copy

    # Hiện danh sách file hiện tại
    if result:
        st.markdown("**📎 File hiện tại:**")
        for fi, fname in enumerate(result):
            fc1, fc2 = st.columns([5,1])
            fc1.markdown(f"📄 `{fname}`")
            if fc2.button("✕", key=f"{key_prefix}_del_f_{fi}", help=f"Xóa {fname}"):
                result.pop(fi)
                st.rerun()
    else:
        st.caption("_(Chưa có file đính kèm)_")

    # Upload thêm file mới
    new_files = st.file_uploader(
        "➕ Thêm file mới",
        accept_multiple_files=True,
        type=["pdf","docx","xlsx","xls","jpg","jpeg","png"],
        key=f"{key_prefix}_uploader"
    )
    if new_files:
        for f in new_files:
            if f.name not in result:
                result.append(f.name)

    return result

# ══════════════════════════════════════════════════════════
# HELPER: header + CSV export
# ══════════════════════════════════════════════════════════
def page_header(title, lst, fname, key=None):
    st.markdown(f'## {title}',
                unsafe_allow_html=True)
    csv_download(lst, fname, key)
    st.write("")

# ══════════════════════════════════════════════════════════
# HELPER: màu status
# ══════════════════════════════════════════════════════════
def c_tt(v):
    s=str(v)
    if "Pass" in s or "Đạt" in s:     return "background:#ebfbee;color:#2b8a3e;font-weight:600"
    if "Failed" in s or "Không" in s:  return "background:#fff5f5;color:#c92a2a;font-weight:600"
    if "Đang" in s:                    return "background:#fff9db;color:#e67700;font-weight:600"
    if "Hoàn" in s or "Đóng" in s:    return "background:#e6fcf5;color:#0ca678;font-weight:600"
    return ""
def c_tinhtrang(v):
    if v=="Sử dụng tốt":    return "background:#ebfbee;color:#2b8a3e;font-weight:600"
    if v=="Chờ hiệu chuẩn": return "background:#fff9db;color:#e67700;font-weight:600"
    if v=="Hỏng":            return "background:#fff5f5;color:#c92a2a;font-weight:600"
    return ""
def pf(lst):
    p=sum(1 for x in lst if x.get("Trạng thái")=="Đạt (Pass)")
    return len(lst),p,len(lst)-p

# ══════════════════════════════════════════════════════════
# ▌ MENU 1: BẢNG ĐIỀU KHIỂN
# ══════════════════════════════════════════════════════════
if page == "📊 Bảng điều khiển":
    st.markdown('## 📊 Bảng điều khiển')
    st.write("")
    il=st.session_state.iqc_list; pl=st.session_state.ipqc_list; ol=st.session_state.oqc_list
    it,ip,if_=pf(il); pt,pp,pf_=pf(pl); ot,op,of_=pf(ol)
    tot=it+pt+ot; totp=ip+pp+op; totf=if_+pf_+of_
    yr=int(totp/tot*100) if tot else 0
    ncr_open=sum(1 for x in st.session_state.ncr_list if x["Trạng thái"] in ["Mở","Đang điều tra"])

    c1,c2,c3,c4=st.columns(4)
    for col,lbl,val,clr in [(c1,"Tổng phiếu kiểm",tot,"#212529"),(c2,"Đạt (Pass)",f"{totp}/{tot}","#2b8a3e"),
                             (c3,"Không đạt",totf,"#c92a2a"),(c4,"Tỷ lệ đạt",f"{yr}%","#1c7ed6")]:
        col.markdown(f'<div class="mc"><p class="mc-label">{lbl}</p><div class="mc-value" style="color:{clr}">{val}</div></div>',unsafe_allow_html=True)
    n1,n2,n3,n4,n5=st.columns(5)
    for col,lbl,val,clr in [
        (n1,"NCR đang mở",ncr_open,"#c92a2a"),
        (n2,"NCR đã xử lý",sum(1 for x in st.session_state.ncr_list if x["Trạng thái"]=="Đã xử lý"),"#364fc7"),
        (n3,"NCR đã đóng",sum(1 for x in st.session_state.ncr_list if x["Trạng thái"]=="Đã đóng"),"#2b8a3e"),
        (n4,"CAPA đang TH",sum(1 for x in st.session_state.capa_list if x["Trạng thái CAPA"]=="Đang tiến hành"),"#f59f00"),
        (n5,"Thiết bị đo",len(st.session_state.dev_list),"#7048e8"),
    ]:
        col.markdown(f'<div class="mc"><p class="mc-label">{lbl}</p><div class="mc-value" style="color:{clr}">{val}</div></div>',unsafe_allow_html=True)
    st.write("")
    c1,c2,c3=st.columns(3)
    for col,icon,bg,fc,title,desc,p,f in [
        (c1,"🛡️","#e7f5ff","#1c7ed6","Kiểm tra đầu vào (IQC)","Kiểm tra nguyên vật liệu đầu vào",ip,if_),
        (c2,"🧪","#ebfbee","#2b8a3e","Kiểm tra quá trình (IPQC)","Kiểm tra trong quá trình sản xuất",pp,pf_),
        (c3,"📦","#fff9db","#f59f00","Kiểm tra thành phẩm (OQC)","Kiểm tra sản phẩm cuối cùng",op,of_),
    ]:
        col.markdown(f'<div class="fc"><div class="fc-icon" style="background:{bg};color:{fc}">{icon}</div><div><div class="fc-title">{title}</div><div class="fc-desc">{desc}</div><div class="fc-sub">Đạt: <b style="color:#2b8a3e">{p}</b> | Không đạt: <b style="color:#c92a2a">{f}</b></div></div></div>',unsafe_allow_html=True)
    c4,c5,c6=st.columns(3)
    for col,icon,bg,fc,title,desc in [
        (c4,"⚠️","#fff5f5","#f03e3e","NCR + CAPA","Sự không phù hợp & hành động khắc phục"),
        (c5,"🔧","#e6fcf5","#0ca678","Thiết bị đo & Hiệu chuẩn","Quản lý thiết bị, lịch hiệu chuẩn"),
        (c6,"📊","#f3f0ff","#7048e8","Báo cáo SPC","Biểu đồ kiểm soát thống kê"),
    ]:
        col.markdown(f'<div class="fc"><div class="fc-icon" style="background:{bg};color:{fc}">{icon}</div><div><div class="fc-title">{title}</div><div class="fc-desc">{desc}</div></div></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ▌ MENU 2: IQC
# ══════════════════════════════════════════════════════════
elif page == "✅ Kiểm tra đầu vào (IQC)":
    page_header("✅ Kiểm tra đầu vào (IQC)", st.session_state.iqc_list, "IQC.csv", "dl_iqc")

    with st.expander("➕ Tạo phiếu IQC mới"):
        with st.form("frm_iqc_new", clear_on_submit=True):
            c1,c2=st.columns(2)
            sp=c1.text_input("Số phiếu *"); da=c2.text_input("Mã dự án")
            kh=c1.text_input("Khách hàng"); vt=c2.text_input("Tên vật tư *")
            nc=c1.text_input("Nhà cung cấp"); lo=c2.text_input("Lô hàng")
            sl=c1.text_input("Số lượng mẫu"); tt=c2.selectbox("Trạng thái",["Đạt (Pass)","Không đạt (Failed)"])
            un=unames()
            nk=c1.selectbox("Người kiểm *",un,index=un.index(cu["Họ tên"]) if cu["Họ tên"] in un else 0)
            ng=c2.date_input("Ngày kiểm",value=date.today())
            gi=c1.time_input("Giờ kiểm",value=datetime.now().time())
            gc=st.text_area("Ghi chú",height=60)
            up=st.file_uploader("📎 Đính kèm file (nhiều file)",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"])
            if st.form_submit_button("✅ Xác nhận tạo phiếu",use_container_width=True):
                if sp and vt:
                    st.session_state.iqc_list.append({
                        "Số phiếu":sp,"Mã dự án":da or "-","Khách hàng":kh or "-",
                        "Tên vật tư":vt,"Nhà cung cấp":nc or "-","Lô":lo or "-","SL mẫu":sl or "-",
                        "Thời gian kiểm":f"{ng.strftime('%d-%m-%Y')} {gi.strftime('%H:%M')}",
                        "Người kiểm":nk,"Files":[f.name for f in up] if up else [],
                        "Trạng thái":tt,"Ghi chú":gc or "-","Người tạo":cu["Tài khoản"],
                    }); ghi_log("IQC","Tạo mới",f"Tạo {sp}"); persist("iqc_list"); st.rerun()
                else: st.error("Vui lòng điền Số phiếu và Tên vật tư")

    def iqc_edit(idx, row):
        with st.form(f"frm_edit_iqc_{idx}", clear_on_submit=False):
            c1,c2=st.columns(2)
            sp=c1.text_input("Số phiếu",value=row.get("Số phiếu",""))
            da=c2.text_input("Mã dự án",value=row.get("Mã dự án",""))
            kh=c1.text_input("Khách hàng",value=row.get("Khách hàng",""))
            vt=c2.text_input("Tên vật tư",value=row.get("Tên vật tư",""))
            nc=c1.text_input("Nhà cung cấp",value=row.get("Nhà cung cấp",""))
            lo=c2.text_input("Lô hàng",value=row.get("Lô",""))
            sl=c1.text_input("SL mẫu",value=row.get("SL mẫu",""))
            un=unames(); cur_nk=row.get("Người kiểm","")
            nk=c2.selectbox("Người kiểm",un,index=un.index(cur_nk) if cur_nk in un else 0)
            tt_opts=["Đạt (Pass)","Không đạt (Failed)"]; cur_tt=row.get("Trạng thái","Đạt (Pass)")
            tt=c1.selectbox("Trạng thái",tt_opts,index=tt_opts.index(cur_tt) if cur_tt in tt_opts else 0)
            gc=st.text_area("Ghi chú",value=row.get("Ghi chú",""),height=60)
            # File management
            st.markdown("**📎 File đính kèm:**")
            cur_files=list(row.get("Files",[]))
            for fi,fn in enumerate(cur_files):
                fa,fb=st.columns([5,1])
                fa.markdown(f"📄 `{fn}`")
                if fb.form_submit_button(f"✕ xóa file {fi+1}",key=f"xf_iqc_{idx}_{fi}"):
                    cur_files.pop(fi); row["Files"]=cur_files; st.rerun()
            new_up=st.file_uploader("➕ Thêm file",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"],key=f"up_iqc_{idx}")
            if st.form_submit_button("💾 Lưu thay đổi",use_container_width=True):
                new_files=cur_files+([f.name for f in new_up] if new_up else [])
                st.session_state.iqc_list[idx].update({
                    "Số phiếu":sp,"Mã dự án":da,"Khách hàng":kh,"Tên vật tư":vt,
                    "Nhà cung cấp":nc,"Lô":lo,"SL mẫu":sl,"Người kiểm":nk,
                    "Trạng thái":tt,"Ghi chú":gc,"Files":new_files
                }); ghi_log("IQC","Cập nhật",f"Sửa {sp}"); persist("iqc_list"); st.rerun()

    render_table_actions(
        st.session_state.iqc_list,"Số phiếu","IQC",
        [("Số phiếu","Số phiếu",1),("Dự án","Mã dự án",1),("Khách hàng","Khách hàng",1.2),
         ("Tên vật tư","Tên vật tư",1.2),("NCC","Nhà cung cấp",1),("Lô","Lô",0.8),
         ("SL","SL mẫu",0.6),("Thời gian","Thời gian kiểm",1.5),("Người kiểm","Người kiểm",1.2),
         ("Files","Files",1.5),("Trạng thái","Trạng thái",1.2),("Ghi chú","Ghi chú",1.2)],
        iqc_edit, badge_col="Trạng thái"
    )

# ══════════════════════════════════════════════════════════
# ▌ MENU 3: IPQC
# ══════════════════════════════════════════════════════════
elif page == "🧪 Kiểm tra quá trình (IPQC)":
    page_header("🧪 Kiểm tra quá trình (IPQC)", st.session_state.ipqc_list, "IPQC.csv","dl_ipqc")

    with st.expander("➕ Tạo phiếu IPQC mới"):
        with st.form("frm_ipqc_new", clear_on_submit=True):
            c1,c2=st.columns(2)
            sp=c1.text_input("Số phiếu *"); da=c2.text_input("Mã dự án")
            kh=c1.text_input("Khách hàng"); cd=c2.text_input("Tên công đoạn *")
            lo=c1.text_input("Lô sản xuất"); sl=c2.text_input("Số lượng mẫu")
            tt=c1.selectbox("Trạng thái",["Đạt (Pass)","Không đạt (Failed)"])
            un=unames()
            nk=c2.selectbox("Người kiểm *",un,index=un.index(cu["Họ tên"]) if cu["Họ tên"] in un else 0)
            ng=c1.date_input("Ngày kiểm",value=date.today())
            gi=c2.time_input("Giờ kiểm",value=datetime.now().time())
            gc=st.text_area("Ghi chú",height=60)
            up=st.file_uploader("📎 Đính kèm file",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"])
            if st.form_submit_button("✅ Xác nhận tạo phiếu",use_container_width=True):
                if sp and cd:
                    st.session_state.ipqc_list.append({
                        "Số phiếu":sp,"Mã dự án":da or "-","Khách hàng":kh or "-",
                        "Tên công đoạn":cd,"Lô":lo or "-","SL mẫu":sl or "-",
                        "Thời gian kiểm":f"{ng.strftime('%d-%m-%Y')} {gi.strftime('%H:%M')}",
                        "Người kiểm":nk,"Files":[f.name for f in up] if up else [],
                        "Trạng thái":tt,"Ghi chú":gc or "-","Người tạo":cu["Tài khoản"],
                    }); ghi_log("IPQC","Tạo mới",f"Tạo {sp}"); persist("ipqc_list"); st.rerun()
                else: st.error("Điền Số phiếu và Tên công đoạn")

    def ipqc_edit(idx,row):
        with st.form(f"frm_edit_ipqc_{idx}", clear_on_submit=False):
            c1,c2=st.columns(2)
            sp=c1.text_input("Số phiếu",value=row.get("Số phiếu",""))
            da=c2.text_input("Mã dự án",value=row.get("Mã dự án",""))
            kh=c1.text_input("Khách hàng",value=row.get("Khách hàng",""))
            cd=c2.text_input("Tên công đoạn",value=row.get("Tên công đoạn",""))
            lo=c1.text_input("Lô",value=row.get("Lô","")); sl=c2.text_input("SL mẫu",value=row.get("SL mẫu",""))
            un=unames(); cur_nk=row.get("Người kiểm","")
            nk=c1.selectbox("Người kiểm",un,index=un.index(cur_nk) if cur_nk in un else 0)
            tt_opts=["Đạt (Pass)","Không đạt (Failed)"]; cur_tt=row.get("Trạng thái","Đạt (Pass)")
            tt=c2.selectbox("Trạng thái",tt_opts,index=tt_opts.index(cur_tt) if cur_tt in tt_opts else 0)
            gc=st.text_area("Ghi chú",value=row.get("Ghi chú",""),height=60)
            st.markdown("**📎 File đính kèm:**")
            cur_files=list(row.get("Files",[]))
            for fi,fn in enumerate(cur_files):
                fa,fb=st.columns([5,1])
                fa.markdown(f"📄 `{fn}`")
                if fb.form_submit_button(f"✕ xóa file {fi+1}",key=f"xf_ipqc_{idx}_{fi}"):
                    cur_files.pop(fi); row["Files"]=cur_files; st.rerun()
            new_up=st.file_uploader("➕ Thêm file",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"],key=f"up_ipqc_{idx}")
            if st.form_submit_button("💾 Lưu thay đổi",use_container_width=True):
                new_files=cur_files+([f.name for f in new_up] if new_up else [])
                st.session_state.ipqc_list[idx].update({
                    "Số phiếu":sp,"Mã dự án":da,"Khách hàng":kh,"Tên công đoạn":cd,
                    "Lô":lo,"SL mẫu":sl,"Người kiểm":nk,"Trạng thái":tt,"Ghi chú":gc,"Files":new_files
                }); ghi_log("IPQC","Cập nhật",f"Sửa {sp}"); persist("ipqc_list"); st.rerun()

    render_table_actions(
        st.session_state.ipqc_list,"Số phiếu","IPQC",
        [("Số phiếu","Số phiếu",1),("Dự án","Mã dự án",1),("Khách hàng","Khách hàng",1.2),
         ("Tên công đoạn","Tên công đoạn",1.5),("Lô","Lô",0.8),("SL","SL mẫu",0.6),
         ("Thời gian","Thời gian kiểm",1.5),("Người kiểm","Người kiểm",1.2),
         ("Files","Files",1.5),("Trạng thái","Trạng thái",1.2),("Ghi chú","Ghi chú",1.2)],
        ipqc_edit, badge_col="Trạng thái"
    )

# ══════════════════════════════════════════════════════════
# ▌ MENU 4: OQC
# ══════════════════════════════════════════════════════════
elif page == "📦 Kiểm tra thành phẩm (OQC)":
    page_header("📦 Kiểm tra thành phẩm (OQC)", st.session_state.oqc_list, "OQC.csv","dl_oqc")

    with st.expander("➕ Tạo phiếu OQC mới"):
        with st.form("frm_oqc_new", clear_on_submit=True):
            c1,c2=st.columns(2)
            sp=c1.text_input("Số phiếu *"); da=c2.text_input("Mã dự án")
            kh=c1.text_input("Khách hàng"); spn=c2.text_input("Mã/Tên sản phẩm *")
            lo=c1.text_input("Lô thành phẩm"); sl=c2.text_input("Số lượng mẫu")
            tt=c1.selectbox("Trạng thái",["Đạt (Pass)","Không đạt (Failed)"])
            un=unames()
            nk=c2.selectbox("Người kiểm *",un,index=un.index(cu["Họ tên"]) if cu["Họ tên"] in un else 0)
            ng=c1.date_input("Ngày kiểm",value=date.today())
            gi=c2.time_input("Giờ kiểm",value=datetime.now().time())
            gc=st.text_area("Ghi chú",height=60)
            up=st.file_uploader("📎 Đính kèm file",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"])
            if st.form_submit_button("✅ Xác nhận tạo phiếu",use_container_width=True):
                if sp and spn:
                    st.session_state.oqc_list.append({
                        "Số phiếu":sp,"Mã dự án":da or "-","Khách hàng":kh or "-",
                        "Mã/Tên SP":spn,"Lô":lo or "-","SL mẫu":sl or "-",
                        "Thời gian kiểm":f"{ng.strftime('%d-%m-%Y')} {gi.strftime('%H:%M')}",
                        "Người kiểm":nk,"Files":[f.name for f in up] if up else [],
                        "Trạng thái":tt,"Ghi chú":gc or "-","Người tạo":cu["Tài khoản"],
                    }); ghi_log("OQC","Tạo mới",f"Tạo {sp}"); persist("oqc_list"); st.rerun()
                else: st.error("Điền Số phiếu và Mã/Tên sản phẩm")

    def oqc_edit(idx,row):
        with st.form(f"frm_edit_oqc_{idx}", clear_on_submit=False):
            c1,c2=st.columns(2)
            sp=c1.text_input("Số phiếu",value=row.get("Số phiếu",""))
            da=c2.text_input("Mã dự án",value=row.get("Mã dự án",""))
            kh=c1.text_input("Khách hàng",value=row.get("Khách hàng",""))
            spn=c2.text_input("Mã/Tên SP",value=row.get("Mã/Tên SP",""))
            lo=c1.text_input("Lô",value=row.get("Lô","")); sl=c2.text_input("SL mẫu",value=row.get("SL mẫu",""))
            un=unames(); cur_nk=row.get("Người kiểm","")
            nk=c1.selectbox("Người kiểm",un,index=un.index(cur_nk) if cur_nk in un else 0)
            tt_opts=["Đạt (Pass)","Không đạt (Failed)"]; cur_tt=row.get("Trạng thái","Đạt (Pass)")
            tt=c2.selectbox("Trạng thái",tt_opts,index=tt_opts.index(cur_tt) if cur_tt in tt_opts else 0)
            gc=st.text_area("Ghi chú",value=row.get("Ghi chú",""),height=60)
            st.markdown("**📎 File đính kèm:**")
            cur_files=list(row.get("Files",[]))
            for fi,fn in enumerate(cur_files):
                fa,fb=st.columns([5,1])
                fa.markdown(f"📄 `{fn}`")
                if fb.form_submit_button(f"✕ xóa file {fi+1}",key=f"xf_oqc_{idx}_{fi}"):
                    cur_files.pop(fi); row["Files"]=cur_files; st.rerun()
            new_up=st.file_uploader("➕ Thêm file",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"],key=f"up_oqc_{idx}")
            if st.form_submit_button("💾 Lưu thay đổi",use_container_width=True):
                new_files=cur_files+([f.name for f in new_up] if new_up else [])
                st.session_state.oqc_list[idx].update({
                    "Số phiếu":sp,"Mã dự án":da,"Khách hàng":kh,"Mã/Tên SP":spn,
                    "Lô":lo,"SL mẫu":sl,"Người kiểm":nk,"Trạng thái":tt,"Ghi chú":gc,"Files":new_files
                }); ghi_log("OQC","Cập nhật",f"Sửa {sp}"); persist("oqc_list"); st.rerun()

    render_table_actions(
        st.session_state.oqc_list,"Số phiếu","OQC",
        [("Số phiếu","Số phiếu",1),("Dự án","Mã dự án",1),("Khách hàng","Khách hàng",1.2),
         ("Mã/Tên SP","Mã/Tên SP",1.5),("Lô","Lô",0.8),("SL","SL mẫu",0.6),
         ("Thời gian","Thời gian kiểm",1.5),("Người kiểm","Người kiểm",1.2),
         ("Files","Files",1.5),("Trạng thái","Trạng thái",1.2),("Ghi chú","Ghi chú",1.2)],
        oqc_edit, badge_col="Trạng thái"
    )

# ══════════════════════════════════════════════════════════
# ▌ MENU 5: NCR + CAPA
# ══════════════════════════════════════════════════════════
elif page == "⚠️ NCR + CAPA":
    st.markdown('## ⚠️ Hệ thống NCR & CAPA')
    st.write("")
    tab1,tab2=st.tabs(["📋 NCR — Sự không phù hợp","🔁 CAPA — Hành động khắc phục"])

    with tab1:
        csv_download(st.session_state.ncr_list,"NCR.csv","dl_ncr")
        with st.expander("➕ Tạo NCR mới"):
            with st.form("frm_ncr_new",clear_on_submit=True):
                c1,c2=st.columns(2)
                so=c1.text_input("Số NCR *"); da=c2.text_input("Mã dự án")
                kh=c1.text_input("Khách hàng"); ten=c2.text_input("Tên vật tư/sản phẩm *")
                lo=c1.text_input("Lô"); sl=c2.text_input("SL phát hiện")
                md=c1.selectbox("Mức độ",["Nhẹ","Vừa","Nghiêm trọng"])
                tt=c2.selectbox("Trạng thái",["Đang điều tra","Mở","Đã xử lý","Đã đóng"])
                un=unames()
                ph=c1.selectbox("Người phát hiện",un,index=un.index(cu["Họ tên"]) if cu["Họ tên"] in un else 0)
                nl=c2.selectbox("Người lập",un,index=un.index(cu["Họ tên"]) if cu["Họ tên"] in un else 0)
                ng=c1.date_input("Ngày",value=date.today()); gi=c2.time_input("Giờ",value=datetime.now().time())
                gc=st.text_area("Ghi chú",height=60)
                up=st.file_uploader("📎 Đính kèm",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"])
                if st.form_submit_button("✅ Tạo NCR",use_container_width=True):
                    if so and ten:
                        st.session_state.ncr_list.append({
                            "Số NCR":so,"Mã dự án":da or "-","Khách hàng":kh or "-",
                            "Tên vật tư/SP":ten,"Lô":lo or "-","SL phát hiện":sl or "-",
                            "Thời gian":f"{ng.strftime('%d-%m-%Y')} {gi.strftime('%H:%M')}",
                            "Người phát hiện":ph,"Mức độ":md,"Trạng thái":tt,
                            "Người lập":nl,"Files":[f.name for f in up] if up else [],"Ghi chú":gc or "-","Người tạo":cu["Tài khoản"],
                        }); ghi_log("NCR","Tạo mới",f"Tạo {so}"); persist("ncr_list"); st.rerun()
                    else: st.error("Điền Số NCR và Tên vật tư/sản phẩm")

        def ncr_edit(idx,row):
            with st.form(f"frm_edit_ncr_{idx}",clear_on_submit=False):
                c1,c2=st.columns(2)
                so=c1.text_input("Số NCR",value=row.get("Số NCR",""))
                da=c2.text_input("Mã dự án",value=row.get("Mã dự án",""))
                kh=c1.text_input("Khách hàng",value=row.get("Khách hàng",""))
                ten=c2.text_input("Tên vật tư/SP",value=row.get("Tên vật tư/SP",""))
                lo=c1.text_input("Lô",value=row.get("Lô","")); sl=c2.text_input("SL phát hiện",value=row.get("SL phát hiện",""))
                md_opts=["Nhẹ","Vừa","Nghiêm trọng"]; cur_md=row.get("Mức độ","Vừa")
                md=c1.selectbox("Mức độ",md_opts,index=md_opts.index(cur_md) if cur_md in md_opts else 0)
                tt_opts=["Đang điều tra","Mở","Đã xử lý","Đã đóng"]; cur_tt=row.get("Trạng thái","Đang điều tra")
                tt=c2.selectbox("Trạng thái",tt_opts,index=tt_opts.index(cur_tt) if cur_tt in tt_opts else 0)
                un_e=unames()
                cur_ph=row.get("Người phát hiện",cu["Họ tên"])
                ph_e=c1.selectbox("Người phát hiện",un_e,index=un_e.index(cur_ph) if cur_ph in un_e else 0,key=f"ph_ncr_{idx}")
                cur_nl=row.get("Người lập",cu["Họ tên"])
                nl_e=c2.selectbox("Người lập",un_e,index=un_e.index(cur_nl) if cur_nl in un_e else 0,key=f"nl_ncr_{idx}")
                gc=st.text_area("Ghi chú",value=row.get("Ghi chú",""),height=60)
                st.markdown("**📎 File đính kèm:**")
                cur_files=list(row.get("Files",[]))
                for fi,fn in enumerate(cur_files):
                    fa,fb=st.columns([5,1])
                    fa.markdown(f"📄 `{fn}`")
                    if fb.form_submit_button(f"✕ xóa file {fi+1}",key=f"xf_ncr_{idx}_{fi}"):
                        cur_files.pop(fi); row["Files"]=cur_files; st.rerun()
                new_up=st.file_uploader("➕ Thêm file",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"],key=f"up_ncr_{idx}")
                if st.form_submit_button("💾 Lưu",use_container_width=True):
                    new_files=cur_files+([f.name for f in new_up] if new_up else [])
                    st.session_state.ncr_list[idx].update({
                        "Số NCR":so,"Mã dự án":da,"Khách hàng":kh,"Tên vật tư/SP":ten,
                        "Lô":lo,"SL phát hiện":sl,"Mức độ":md,"Trạng thái":tt,
                        "Người phát hiện":ph_e,"Người lập":nl_e,"Ghi chú":gc,"Files":new_files
                    }); ghi_log("NCR","Cập nhật",f"Sửa {so}"); persist("ncr_list"); st.rerun()

        render_table_actions(
            st.session_state.ncr_list,"Số NCR","NCR",
            [("Số NCR","Số NCR",1),("Dự án","Mã dự án",0.9),("Khách hàng","Khách hàng",1.1),
             ("Tên vật tư/SP","Tên vật tư/SP",1.5),("Lô","Lô",0.7),("SL","SL phát hiện",0.8),
             ("Thời gian","Thời gian",1.4),("Người PH","Người phát hiện",1.1),
             ("Người lập","Người lập",1.1),("Mức độ","Mức độ",0.8),
             ("Trạng thái","Trạng thái",1.2),("Files","Files",1.2)],
            ncr_edit, badge_col="Trạng thái", all_users=True
        )

    with tab2:
        csv_download(st.session_state.capa_list,"CAPA.csv","dl_capa")
        with st.expander("➕ Tạo CAPA mới"):
            with st.form("frm_capa_new",clear_on_submit=True):
                c1,c2=st.columns(2)
                ma=c1.text_input("Mã CAPA *"); ncr=c2.text_input("Số NCR liên kết")
                bp=c1.text_input("Bộ phận"); th=c2.date_input("Thời hạn",value=date.today())
                tt=c1.selectbox("Trạng thái CAPA",["Đang tiến hành","Hoàn thành","Quá hạn"])
                un_c=unames()
                nl_c=c2.selectbox("Người lập",un_c,index=un_c.index(cu["Họ tên"]) if cu["Họ tên"] in un_c else 0)
                nn=st.text_area("Nguyên nhân gốc rễ",height=60)
                kp=st.text_area("Hành động khắc phục",height=60)
                pn=st.text_area("Hành động phòng ngừa",height=60)
                gc=st.text_area("Ghi chú",height=50)
                up=st.file_uploader("📎 Đính kèm",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"])
                if st.form_submit_button("✅ Tạo CAPA",use_container_width=True):
                    if ma:
                        st.session_state.capa_list.append({
                            "Mã CAPA":ma,"Số NCR":ncr or "-","Nguyên nhân":nn or "-",
                            "Khắc phục":kp or "-","Phòng ngừa":pn or "-","Bộ phận":bp or "-",
                            "Thời hạn":th.strftime("%d-%m-%Y"),"Trạng thái CAPA":tt,
                            "Files":[f.name for f in up] if up else [],"Ghi chú":gc or "-","Người tạo":cu["Tài khoản"],
                        }); ghi_log("CAPA","Tạo mới",f"Tạo {ma}"); persist("capa_list"); st.rerun()
                    else: st.error("Điền Mã CAPA")

        def capa_edit(idx,row):
            with st.form(f"frm_edit_capa_{idx}",clear_on_submit=False):
                c1,c2=st.columns(2)
                ma=c1.text_input("Mã CAPA",value=row.get("Mã CAPA",""))
                ncr=c2.text_input("Số NCR",value=row.get("Số NCR",""))
                bp=c1.text_input("Bộ phận",value=row.get("Bộ phận",""))
                th=c2.text_input("Thời hạn",value=row.get("Thời hạn",""))
                tt_opts=["Đang tiến hành","Hoàn thành","Quá hạn"]; cur_tt=row.get("Trạng thái CAPA","Đang tiến hành")
                tt=c1.selectbox("Trạng thái CAPA",tt_opts,index=tt_opts.index(cur_tt) if cur_tt in tt_opts else 0)
                nn=st.text_area("Nguyên nhân",value=row.get("Nguyên nhân",""),height=60)
                kp=st.text_area("Khắc phục",value=row.get("Khắc phục",""),height=60)
                pn=st.text_area("Phòng ngừa",value=row.get("Phòng ngừa",""),height=60)
                un_ce=unames(); cur_nl_ce=row.get("Người lập",cu["Họ tên"])
                nl_ce=st.selectbox("Người lập",un_ce,index=un_ce.index(cur_nl_ce) if cur_nl_ce in un_ce else 0,key=f"nl_capa_{idx}")
                gc=st.text_area("Ghi chú",value=row.get("Ghi chú",""),height=50)
                st.markdown("**📎 File đính kèm:**")
                cur_files=list(row.get("Files",[]))
                for fi,fn in enumerate(cur_files):
                    fa,fb=st.columns([5,1])
                    fa.markdown(f"📄 `{fn}`")
                    if fb.form_submit_button(f"✕ xóa file {fi+1}",key=f"xf_capa_{idx}_{fi}"):
                        cur_files.pop(fi); row["Files"]=cur_files; st.rerun()
                new_up=st.file_uploader("➕ Thêm file",accept_multiple_files=True,type=["pdf","docx","xlsx","xls","jpg","jpeg","png"],key=f"up_capa_{idx}")
                if st.form_submit_button("💾 Lưu",use_container_width=True):
                    new_files=cur_files+([f.name for f in new_up] if new_up else [])
                    st.session_state.capa_list[idx].update({
                        "Mã CAPA":ma,"Số NCR":ncr,"Bộ phận":bp,"Thời hạn":th,
                        "Trạng thái CAPA":tt,"Nguyên nhân":nn,"Khắc phục":kp,
                        "Phòng ngừa":pn,"Người lập":nl_ce,"Ghi chú":gc,"Files":new_files
                    }); ghi_log("CAPA","Cập nhật",f"Sửa {ma}"); persist("capa_list"); st.rerun()

        render_table_actions(
            st.session_state.capa_list,"Mã CAPA","CAPA",
            [("Mã CAPA","Mã CAPA",1),("Số NCR","Số NCR",1),("Nguyên nhân","Nguyên nhân",1.8),
             ("Khắc phục","Khắc phục",1.8),("Bộ phận","Bộ phận",1),("Thời hạn","Thời hạn",1.1),
             ("Người lập","Người lập",1.1),("Trạng thái","Trạng thái CAPA",1.3),("Files","Files",1.2)],
            capa_edit, badge_col="Trạng thái CAPA", all_users=True
        )

# ══════════════════════════════════════════════════════════
# ▌ MENU 6: THIẾT BỊ ĐO
# ══════════════════════════════════════════════════════════
elif page == "🔧 Thiết bị đo":
    page_header("🔧 Thiết bị đo & Hiệu chuẩn", st.session_state.dev_list, "Devices.csv","dl_dev")

    if "show_dev_form" not in st.session_state:
        st.session_state.show_dev_form = False
    if st.button("➕ Đăng ký thiết bị mới", key="btn_show_dev_form"):
        st.session_state.show_dev_form = True

    if st.session_state.show_dev_form:
        with st.container():
            st.markdown("---")
            st.markdown("#### ➕ Đăng ký thiết bị mới")
            with st.form("frm_dev_new", clear_on_submit=True):
                c1,c2=st.columns(2)
                ma=c1.text_input("Mã TB *"); ten=c2.text_input("Tên thiết bị *")
                ser=c1.text_input("Số serie"); vt=c2.text_input("Vị trí")
                ck=c1.selectbox("Chu kỳ HC",["06 tháng","12 tháng"])
                tt=c2.selectbox("Tình trạng",["Sử dụng tốt","Chờ hiệu chuẩn","Hỏng"])
                last=c1.date_input("HC lần cuối",value=date.today())
                nxt=c2.date_input("Hạn HC",value=date.today())
                un_d=unames()
                nl_d=st.selectbox("Người lập",un_d,index=un_d.index(cu["Họ tên"]) if cu["Họ tên"] in un_d else 0)
                gc=st.text_input("Ghi chú")
                btn_ok, btn_cancel, _ = st.columns([1.5, 1.5, 6])
                submitted = btn_ok.form_submit_button("✅ Đăng ký", use_container_width=True)
                cancelled = btn_cancel.form_submit_button("❌ Hủy", use_container_width=True)
                if submitted:
                    if ma and ten:
                        st.session_state.dev_list.append({
                            "Mã TB":ma,"Tên thiết bị":ten,"Số serie":ser or "-","Vị trí":vt or "-",
                            "Chu kỳ HC":ck,"HC lần cuối":last.strftime("%d-%m-%Y"),
                            "Hạn HC":nxt.strftime("%d-%m-%Y"),"Tình trạng":tt,
                            "Người lập":nl_d,"Ghi chú":gc or "-","Người tạo":cu["Tài khoản"],
                        })
                        ghi_log("TB","Đăng ký",f"Đăng ký {ma}")
                        persist("dev_list")
                        st.session_state.show_dev_form = False
                        st.rerun()
                    else:
                        st.error("Vui lòng điền Mã TB và Tên thiết bị")
                if cancelled:
                    st.session_state.show_dev_form = False
                    st.rerun()
            st.markdown("---")

    def dev_edit(idx,row):
        with st.form(f"frm_edit_dev_{idx}",clear_on_submit=False):
            c1,c2=st.columns(2)
            ma=c1.text_input("Mã TB",value=row.get("Mã TB",""))
            ten=c2.text_input("Tên thiết bị",value=row.get("Tên thiết bị",""))
            ser=c1.text_input("Số serie",value=row.get("Số serie",""))
            vt=c2.text_input("Vị trí",value=row.get("Vị trí",""))
            ck_o=["06 tháng","12 tháng"]; cur_ck=row.get("Chu kỳ HC","12 tháng")
            ck=c1.selectbox("Chu kỳ HC",ck_o,index=ck_o.index(cur_ck) if cur_ck in ck_o else 0)
            tt_o=["Sử dụng tốt","Chờ hiệu chuẩn","Hỏng"]; cur_tt=row.get("Tình trạng","Sử dụng tốt")
            tt=c2.selectbox("Tình trạng",tt_o,index=tt_o.index(cur_tt) if cur_tt in tt_o else 0)
            last=c1.text_input("HC lần cuối",value=row.get("HC lần cuối",""))
            nxt=c2.text_input("Hạn HC",value=row.get("Hạn HC",""))
            un_de=unames(); cur_nl_de=row.get("Người lập",cu["Họ tên"])
            nl_de=c1.selectbox("Người lập",un_de,
                index=un_de.index(cur_nl_de) if cur_nl_de in un_de else 0,
                key=f"nl_dev_{idx}")
            gc=c2.text_input("Ghi chú",value=row.get("Ghi chú",""))
            if st.form_submit_button("💾 Lưu",use_container_width=True):
                st.session_state.dev_list[idx].update({
                    "Mã TB":ma,"Tên thiết bị":ten,"Số serie":ser,"Vị trí":vt,
                    "Chu kỳ HC":ck,"HC lần cuối":last,"Hạn HC":nxt,"Tình trạng":tt,
                    "Người lập":nl_de,"Ghi chú":gc
                }); ghi_log("TB","Cập nhật",f"Sửa {ma}"); persist("dev_list"); st.rerun()

    render_table_actions(
        st.session_state.dev_list,"Mã TB","TB",
        [("Mã TB","Mã TB",1),("Tên thiết bị","Tên thiết bị",1.5),("Số serie","Số serie",1),
         ("Vị trí","Vị trí",1),("Chu kỳ HC","Chu kỳ HC",1),("HC lần cuối","HC lần cuối",1.2),
         ("Hạn HC","Hạn HC",1.2),("Người lập","Người lập",1.1),
         ("Tình trạng","Tình trạng",1.2),("Ghi chú","Ghi chú",1.2)],
        dev_edit,
        badge_col="Tình trạng",
        badge_fn=badge_tinhtrang,
        search_fields=["Mã TB","Tên thiết bị","Số serie","Vị trí","Tình trạng","Người lập"],
        all_users=True,
    )

# ══════════════════════════════════════════════════════════
# ▌ MENU 7: BÁO CÁO SPC — ĐẦY ĐỦ
# ══════════════════════════════════════════════════════════
elif page == "📊 Báo cáo (SPC)":
    st.markdown('## 📊 Báo cáo thống kê (SPC)')
    st.write("")

    # ── 3 thẻ tóm tắt IQC / OQC / IPQC ──────────────────────────
    il=st.session_state.iqc_list; pl=st.session_state.ipqc_list; ol=st.session_state.oqc_list
    it,ip,if_=pf(il); pt,pp,pf_=pf(pl); ot,op,of_=pf(ol)
    sc1,sc2,sc3=st.columns(3)
    for col,lbl,tot,pas,fail in [(sc1,"IQC",it,ip,if_),(sc2,"OQC",ot,op,of_),(sc3,"IPQC",pt,pp,pf_)]:
        yr_=int(pas/tot*100) if tot else 0
        col.markdown(f"""<div class="spc-card">
          <div class="spc-title">{lbl}</div>
          <div class="spc-row">
            <div style="min-width:70px"><div class="spc-stat-label">Tổng</div><div class="spc-stat-val">{tot}</div></div>
            <div style="min-width:70px"><div class="spc-stat-label">Đạt</div><div class="spc-stat-val" style="color:#2b8a3e">{pas}</div></div>
            <div style="min-width:80px"><div class="spc-stat-label">Không đạt</div><div class="spc-stat-val" style="color:#c92a2a">{fail}</div></div>
          </div>
          <div style="margin-top:10px">
            <span class="badge badge-{'pass' if yr_>=80 else 'fail'}">Tỷ lệ đạt: {yr_}%</span>
          </div>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # ── Import dữ liệu đo từ nhà máy ─────────────────────────────
    with st.expander("📂 Import bảng kết quả đo từ factory (Excel / CSV)"):
        st.markdown("""
**Yêu cầu định dạng file:**
- Cột đầu tiên: **Mẫu** (tên hoặc số thứ tự mẫu)
- Các cột tiếp theo: **giá trị đo** (số thực, ví dụ: Chiều dày, Chiều rộng...)
- Định dạng: `.xlsx`, `.xls`, hoặc `.csv`
        """)
        up_spc = st.file_uploader("Chọn file kết quả đo", type=["xlsx","xls","csv"], key="spc_upload")
        if up_spc:
            try:
                is_csv = up_spc.name.endswith(".csv")

                # ── Bước 1: Đọc thô toàn bộ, không header ──
                up_spc.seek(0)
                if is_csv:
                    df_raw_full = pd.read_csv(up_spc, header=None, dtype=str)
                else:
                    df_raw_full = pd.read_excel(up_spc, header=None, dtype=str)

                # ── Bước 2: Tìm hàng header đúng ──
                # Header thật: nhiều ô text (tên cột), hàng kế tiếp nhiều số
                # Dùng text_i*3 để phân biệt header (nhiều text) vs data row (nhiều số)
                header_row = 0
                best_score = -1
                for i in range(min(5, len(df_raw_full) - 1)):
                    row_i    = df_raw_full.iloc[i]
                    row_next = df_raw_full.iloc[i + 1]
                    non_empty = sum(1 for v in row_i if str(v).strip() not in ("","nan","None"))
                    num_next  = sum(1 for v in row_next
                                    if pd.to_numeric(str(v).strip(), errors="coerce")
                                    == pd.to_numeric(str(v).strip(), errors="coerce"))
                    # Số ô TEXT thuần (không phải số) trong hàng i — header có nhiều text hơn data
                    text_i = sum(1 for v in row_i
                                 if str(v).strip() not in ("","nan","None")
                                 and pd.to_numeric(str(v).strip(), errors="coerce")
                                 != pd.to_numeric(str(v).strip(), errors="coerce"))
                    score = non_empty + num_next * 2 + text_i * 3
                    if score > best_score and non_empty >= 2:
                        best_score = score
                        header_row = i

                # ── Bước 3: Đọc lại với header đúng, giữ nguyên kiểu dữ liệu ──
                up_spc.seek(0)
                if is_csv:
                    df_imp = pd.read_csv(up_spc, header=header_row, keep_default_na=False)
                else:
                    df_imp = pd.read_excel(up_spc, header=header_row, keep_default_na=False)

                # Bỏ hàng hoàn toàn trống
                df_imp = df_imp.dropna(how="all").reset_index(drop=True)

                # Hiển thị kết quả
                num_cols_found = df_imp.select_dtypes(include="number").columns.tolist()
                text_cols_found = [c for c in df_imp.columns if c not in num_cols_found]

                st.success(
                    f"✅ Tải thành công: **{len(df_imp)} mẫu** × **{len(df_imp.columns)} cột**  ·  "
                    f"Cột số ({len(num_cols_found)}): **{', '.join(str(c) for c in num_cols_found)}**  ·  "
                    f"Cột nhãn: {', '.join(str(c) for c in text_cols_found)}"
                )
                st.dataframe(df_imp, use_container_width=True, hide_index=True)
                st.session_state.spc_df = df_imp

            except Exception as e:
                st.error(f"Lỗi đọc file: {e}")
                import traceback
                st.code(traceback.format_exc())

    st.write("")

    # ── Chuẩn bị dữ liệu SPC ─────────────────────────────────────
    default_vals = np.array([50.05,49.98,50.12,49.91,50.02,50.08,49.95,50.15,50.01,49.99,
                              50.03,49.97,50.07,49.94,50.11,50.00,49.96,50.09,49.93,50.06])
    default_labels = [f"M{i+1}" for i in range(len(default_vals))]

    if st.session_state.spc_df is not None:
        df_raw = st.session_state.spc_df

        # Xác định cột số đo (bỏ cột ID nếu có) và cột nhãn mẫu
        num_cols  = df_raw.select_dtypes(include="number").columns.tolist()
        # Bỏ cột "ID" hoặc cột index thuần (thường là cột số đầu tiên tên ID/STT/No)
        id_like   = [c for c in num_cols if str(c).strip().upper() in ("ID","STT","NO","#","SỐ")]
        meas_cols = [c for c in num_cols if c not in id_like]
        text_cols = [c for c in df_raw.columns if c not in num_cols]
        # Cột nhãn mẫu = cột text đầu tiên (ưu tiên cột tên "Mẫu")
        mau_col_candidates = [c for c in text_cols if "mẫu" in str(c).lower() or "sample" in str(c).lower() or "name" in str(c).lower()]
        lbl_col = mau_col_candidates[0] if mau_col_candidates else (text_cols[0] if text_cols else None)

        if meas_cols:
            st.markdown("**📐 Chọn mẫu để phân tích:**")
            # Mỗi HÀNG = 1 loại mẫu, các cột đo = lần đo 1,2,3...
            if lbl_col and lbl_col in df_raw.columns:
                row_options = {str(df_raw.loc[i, lbl_col]): i for i in df_raw.index}
            else:
                row_options = {f"Mẫu {i+1}": i for i in df_raw.index}

            sel_row_name = st.selectbox(
                "Chọn loại mẫu / sản phẩm:",
                list(row_options.keys()), key="spc_row_sel"
            )
            sel_row_idx = row_options[sel_row_name]

            # Lấy các giá trị đo của hàng được chọn
            raw_vals = [df_raw.loc[sel_row_idx, c] for c in meas_cols]
            vals = np.array([float(v) for v in raw_vals if pd.to_numeric(v, errors="coerce") == pd.to_numeric(v, errors="coerce")])
            labels = [str(c) for c in meas_cols[:len(vals)]]

            st.caption(f"📌 Phân tích: **{sel_row_name}** — {len(vals)} lần đo: {', '.join(labels)}")
        else:
            st.warning("Không tìm thấy cột số đo trong file.")
            vals, labels = default_vals, default_labels
    else:
        vals, labels = default_vals, default_labels
        st.caption("*(Đang hiển thị dữ liệu mẫu — import file để dùng số liệu thực tế)*")

    mean_v = float(np.mean(vals))
    std_v  = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
    ucl_v  = mean_v + 3 * std_v
    lcl_v  = mean_v - 3 * std_v
    out_of_ctrl = int(np.sum((vals > ucl_v) | (vals < lcl_v)))

    # ── 3 tab biểu đồ ────────────────────────────────────────────
    t1, t2, t3 = st.tabs(["📈 Biểu đồ kiểm soát (X-bar & Histogram)",
                           "📊 Biểu đồ Pareto (tần suất lỗi)",
                           "📉 Xu hướng & Range Chart"])

    # ── TAB 1: X-bar chart + Histogram ───────────────────────────
    with t1:
        # KPI metrics
        m1,m2,m3,m4,m5 = st.columns(5)
        m1.metric("Mean (CL)", f"{mean_v:.4f}")
        m2.metric("UCL (+3σ)", f"{ucl_v:.4f}")
        m3.metric("LCL (−3σ)", f"{lcl_v:.4f}")
        m4.metric("Std Dev (σ)", f"{std_v:.4f}")
        delta_color = "inverse" if out_of_ctrl > 0 else "normal"
        m5.metric("⚠️ Ngoài giới hạn", out_of_ctrl, delta=f"/{len(vals)} mẫu", delta_color=delta_color)

        st.write("")
        bc1, bc2 = st.columns(2)

        with bc1:
            st.markdown("**X-bar Control Chart**")
            df_xbar = pd.DataFrame({
                "Mẫu":   labels,
                "Giá trị đo": vals,
                "UCL":   [ucl_v]*len(vals),
                "CL":    [mean_v]*len(vals),
                "LCL":   [lcl_v]*len(vals),
            }).set_index("Mẫu")
            st.line_chart(df_xbar, color=["#1c7ed6","#f03e3e","#2b8a3e","#f03e3e"])
            st.caption("🔵 Giá trị đo  🔴 UCL/LCL  🟢 CL (Mean)")

        with bc2:
            st.markdown("**Histogram — Phân bố giá trị đo**")
            hist, edges = np.histogram(vals, bins=min(8, max(4, len(vals)//3)))
            df_hist = pd.DataFrame({
                "Khoảng": [f"{edges[i]:.3f}–{edges[i+1]:.3f}" for i in range(len(hist))],
                "Tần số": hist,
            }).set_index("Khoảng")
            st.bar_chart(df_hist, color="#1c7ed6")

        # Bảng chi tiết mẫu ngoài giới hạn
        out_rows = [(labels[i], float(vals[i])) for i in range(len(vals)) if vals[i] > ucl_v or vals[i] < lcl_v]
        if out_rows:
            st.markdown("**⚠️ Mẫu ngoài giới hạn kiểm soát:**")
            df_out = pd.DataFrame(out_rows, columns=["Mẫu","Giá trị đo"])
            df_out["Lệch so với Mean"] = (df_out["Giá trị đo"] - mean_v).round(4)
            df_out["Đánh giá"] = df_out["Giá trị đo"].apply(
                lambda v: "⬆️ Vượt UCL" if v > ucl_v else "⬇️ Dưới LCL")
            st.dataframe(df_out.style.map(
                lambda v: "color:#c92a2a;font-weight:600" if "Vượt" in str(v) or "Dưới" in str(v) else "",
                subset=["Đánh giá"]
            ), use_container_width=True, hide_index=True)

    # ── TAB 2: Pareto ─────────────────────────────────────────────
    with t2:
        ncr_data = st.session_state.ncr_list
        if ncr_data:
            cnt = Counter(x.get("Tên vật tư/SP","-") for x in ncr_data)
            df_par = pd.DataFrame({"Dạng lỗi": list(cnt.keys()), "Số vụ": list(cnt.values())})
            df_par = df_par.sort_values("Số vụ", ascending=False).reset_index(drop=True)
            st.caption("*(Dữ liệu từ phân hệ NCR thực tế)*")
        else:
            df_par = pd.DataFrame({
                "Dạng lỗi": ["Trầy xước bề mặt","Móp méo biến dạng","Lỗi bọt khí kính","Sai kích thước","Lệch màu sơn"],
                "Số vụ":    [45, 28, 12, 6, 3]
            })
            st.caption("*(Dữ liệu mẫu — khi có NCR thực tế sẽ tự cập nhật)*")

        total_loi = df_par["Số vụ"].sum()
        df_par["% vụ"] = (df_par["Số vụ"] / total_loi * 100).round(1)
        df_par["% tích lũy"] = df_par["% vụ"].cumsum().round(1)

        pc1, pc2 = st.columns([3,2])
        with pc1:
            st.markdown("**Biểu đồ Pareto — Tần suất dạng lỗi**")
            st.bar_chart(df_par.set_index("Dạng lỗi")["Số vụ"], color="#f03e3e")
        with pc2:
            st.markdown("**Bảng chi tiết**")
            df_par_show = df_par.copy()
            df_par_show["% vụ"] = df_par_show["% vụ"].apply(lambda x: f"{x:.1f}%")
            df_par_show["% tích lũy"] = df_par_show["% tích lũy"].apply(lambda x: f"{x:.1f}%")
            st.dataframe(df_par_show.style.set_properties(**{"font-size":"13px"})
                .bar(subset=["Số vụ"], color="#ffd8a8"),
                use_container_width=True, hide_index=True)

        # Quy tắc 80/20
        top_causes = df_par[df_par["% tích lũy"] <= 80]["Dạng lỗi"].tolist()
        if not top_causes:
            top_causes = [df_par.iloc[0]["Dạng lỗi"]]
        st.info(f"📌 **Quy tắc Pareto 80/20:** {len(top_causes)} dạng lỗi chiếm ~80% tổng sự cố: "
                f"**{', '.join(top_causes)}**")

    # ── TAB 3: Xu hướng + Range Chart ────────────────────────────
    with t3:
        rc1, rc2 = st.columns(2)

        with rc1:
            st.markdown("**Range Chart — Biên độ dao động liên tiếp**")
            ranges = np.abs(np.diff(vals, prepend=vals[0]))
            r_mean = float(ranges.mean())
            r_ucl  = r_mean * 3.267  # hệ số D4 với n=2
            df_range = pd.DataFrame({
                "Mẫu":  labels,
                "Range":  ranges,
                "UCL_R":  [r_ucl]*len(ranges),
                "CL_R":   [r_mean]*len(ranges),
            }).set_index("Mẫu")
            st.line_chart(df_range, color=["#f59f00","#f03e3e","#2b8a3e"])
            st.caption("🟠 Range  🔴 UCL_R  🟢 CL_R")

        with rc2:
            st.markdown("**Moving Average — Xu hướng trung bình động**")
            window = min(5, max(2, len(vals)//4))
            ma_series = pd.Series(vals).rolling(window, min_periods=1).mean().values
            df_ma = pd.DataFrame({
                "Mẫu":            labels,
                "Giá trị đo":     vals,
                f"MA({window})":  ma_series,
            }).set_index("Mẫu")
            st.line_chart(df_ma, color=["#adb5bd","#1c7ed6"])
            st.caption(f"🔵 MA({window})  ⚪ Giá trị thực")

        # Bảng tóm tắt thống kê
        st.write("")
        st.markdown("**📋 Tóm tắt thống kê mô tả**")
        stats = {
            "Chỉ số": ["N (mẫu)","Min","Max","Mean","Median","Std Dev (σ)","UCL (+3σ)","LCL (−3σ)","Cp (ước tính)"],
            "Giá trị": [
                len(vals),
                f"{float(np.min(vals)):.4f}",
                f"{float(np.max(vals)):.4f}",
                f"{mean_v:.4f}",
                f"{float(np.median(vals)):.4f}",
                f"{std_v:.4f}",
                f"{ucl_v:.4f}",
                f"{lcl_v:.4f}",
                f"{((ucl_v-lcl_v)/(6*std_v)):.3f}" if std_v > 0 else "N/A",
            ]
        }
        df_stats = pd.DataFrame(stats)
        st.dataframe(df_stats.style.set_properties(**{"font-size":"13px","padding":"7px 10px"}),
                     use_container_width=False, hide_index=True)

        # Nhận xét tự động
        cp_val = (ucl_v - lcl_v) / (6 * std_v) if std_v > 0 else 0
        st.write("")
        if cp_val >= 1.33:
            st.success(f"✅ Cp = {cp_val:.3f} ≥ 1.33 — Quy trình **có năng lực tốt**, kiểm soát ổn định.")
        elif cp_val >= 1.0:
            st.warning(f"⚠️ Cp = {cp_val:.3f} — Quy trình **đạt tối thiểu**, cần theo dõi chặt.")
        else:
            st.error(f"❌ Cp = {cp_val:.3f} < 1.0 — Quy trình **không đủ năng lực**, cần cải thiện ngay.")

# ══════════════════════════════════════════════════════════
# ▌ MENU 8: NHẬT KÝ
# ══════════════════════════════════════════════════════════
elif page == "📜 Nhật ký hoạt động":
    page_header("📜 Nhật ký hoạt động", st.session_state.log_list, "Logs.csv","dl_log")

    # ── Backup & Restore — chỉ Quản lý và Trưởng QC ──
    if cu["Vai trò"] in ["Quản lý", "Trưởng QC"]:
        with st.expander("💾 Sao lưu & Khôi phục dữ liệu"):
            bc1, bc2 = st.columns(2)
            with bc1:
                st.markdown("**📦 Sao lưu toàn bộ dữ liệu**")
                st.caption("Tải file backup JSON chứa tất cả phiếu, tài khoản, nhật ký.")
                bk_data = backup_json(st.session_state)
                st.download_button("📥 Tải file backup",data=bk_data,
                    file_name=f"QualityMES_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json", key="btn_backup")
            with bc2:
                st.markdown("**🔄 Khôi phục từ backup**")
                st.caption("Upload file backup JSON để khôi phục dữ liệu.")
                up_restore = st.file_uploader("Chọn file backup",type=["json"],key="up_restore")
                if up_restore:
                    ok, msg = restore_json(up_restore.read(), st.session_state)
                    if ok: st.success(msg); st.rerun()
                    else: st.error(msg)
    else:
        st.info("🔒 Chức năng Sao lưu & Khôi phục chỉ dành cho Quản lý và Trưởng QC.")
    st.write("")

    df_l=pd.DataFrame(st.session_state.log_list)
    if not df_l.empty:
        st.dataframe(df_l.style.set_properties(**{"font-size":"13px","padding":"7px 10px"})
            .set_table_styles([{"selector":"thead th","props":[("background","#f1f3f5"),("font-weight","700"),("font-size","12px"),("color","#495057")]}]),
            use_container_width=True,hide_index=True)
    else: st.info("Nhật ký trống")

# ══════════════════════════════════════════════════════════
# ▌ MENU 9: QUẢN LÝ NGƯỜI DÙNG
# ══════════════════════════════════════════════════════════
elif page == "👤 Quản lý người dùng":
    st.markdown('## 👤 Quản lý người dùng & Phân quyền')
    st.write("")
    role=cu["Vai trò"]

    # Ma trận phân quyền
    with st.expander("📖 Ma trận phân quyền hệ thống"):
        df_pq=pd.DataFrame({
            "Quyền hạn":["Tạo TK Quản lý","Tạo TK Trưởng QC","Tạo TK Kiểm tra viên",
                         "Xóa tài khoản bất kỳ","Xóa TK Kiểm tra viên","Reset pass mọi TK",
                         "Tự đổi pass của mình","Tạo phiếu mới","Sửa/Xóa phiếu của mình",
                         "Sửa/Xóa phiếu của người khác","Xem toàn bộ dữ liệu"],
            "Quản lý (Admin)": ["✅","✅","✅","✅","✅","✅","✅","✅","✅","✅","✅"],
            "Trưởng QC":       ["❌","❌","✅","❌","✅","❌","✅","✅","✅","✅","✅"],
            "Kiểm tra viên":   ["❌","❌","❌","❌","❌","❌","✅","✅","✅","❌","✅ (đọc)"],
        })
        st.dataframe(df_pq,use_container_width=True,hide_index=True)

    st.write("")

    # Tạo tài khoản mới
    # Admin tạo được: Quản lý, Trưởng QC, KTV
    # Trưởng QC tạo được: chỉ KTV
    if role in ["Quản lý","Trưởng QC"]:
        with st.expander("➕ Tạo tài khoản nhân sự mới"):
            with st.form("frm_user_new",clear_on_submit=True):
                c1,c2=st.columns(2)
                nm=c1.text_input("Họ và tên *"); un=c2.text_input("Tên tài khoản *")
                pw=c1.text_input("Mật khẩu *",type="password")
                ro_opts=["Quản lý","Trưởng QC","Kiểm tra viên"] if role=="Quản lý" else ["Kiểm tra viên"]
                ro=c2.selectbox("Phân quyền",ro_opts)
                if st.form_submit_button("💾 Tạo tài khoản",use_container_width=True):
                    if nm and un and pw:
                        if any(u["Tài khoản"]==un for u in st.session_state.users_list):
                            st.error("Tên tài khoản đã tồn tại!")
                        else:
                            st.session_state.users_list.append({"Tài khoản":un,"Họ tên":nm,"Mật khẩu":pw,"Phân quyền":ro,"Trạng thái":"Hoạt động"})
                            ghi_log("Users","Tạo TK",f"Tạo {un} ({ro})"); persist("users_list"); st.success(f"✅ Đã tạo {nm}"); st.rerun()
                    else: st.error("Điền đầy đủ họ tên, tài khoản, mật khẩu")

    st.write("")

    # Bảng users
    def c_role(v):
        if v=="Quản lý":       return "background:#e7f5ff;color:#1c7ed6;font-weight:600"
        if v=="Trưởng QC":     return "background:#ebfbee;color:#2b8a3e;font-weight:600"
        if v=="Kiểm tra viên": return "background:#f3f0ff;color:#7048e8;font-weight:600"
        return ""
    ud=[]
    for u in st.session_state.users_list:
        show=role=="Quản lý" or u["Tài khoản"]==cu["Tài khoản"]
        ud.append({"Họ và tên":u["Họ tên"],"Tài khoản":u["Tài khoản"],
                   "Mật khẩu":u["Mật khẩu"] if show else "••••••",
                   "Phân quyền":u["Phân quyền"],"Trạng thái":u["Trạng thái"]})
    st.dataframe(pd.DataFrame(ud).style.map(c_role,subset=["Phân quyền"])
        .set_properties(**{"font-size":"13px","padding":"7px 10px"})
        .set_table_styles([{"selector":"thead th","props":[("background","#f1f3f5"),("font-weight","700"),("font-size","12px"),("color","#495057")]}]),
        use_container_width=True,hide_index=True)

    st.write("")
    # ── Xóa hàng loạt tài khoản (Admin only) ──
    if role == "Quản lý":
        with st.expander("🗑️ Xóa hàng loạt tài khoản (Admin)"):
            st.warning("⚠️ Chỉ dùng khi muốn xóa tài khoản mẫu và tạo lại tài khoản thật.")
            # Danh sách checkbox các tài khoản có thể xóa (trừ admin hiện tại)
            deletable = [u for u in st.session_state.users_list if u["Tài khoản"] != "admin"]
            if deletable:
                del_names = [f"{u['Họ tên']} ({u['Tài khoản']}) — {u['Phân quyền']}" for u in deletable]
                selected = st.multiselect("Chọn tài khoản muốn xóa:", del_names, key="bulk_del_sel")
                if selected:
                    if st.button(f"🗑️ Xóa {len(selected)} tài khoản đã chọn", type="primary", key="btn_bulk_del"):
                        sel_accounts = [s.split("(")[1].split(")")[0] for s in selected]
                        st.session_state.users_list = [
                            u for u in st.session_state.users_list
                            if u["Tài khoản"] not in sel_accounts
                        ]
                        ghi_log("Users","Xóa hàng loạt",f"Xóa {len(sel_accounts)} tài khoản: {', '.join(sel_accounts)}")
                        st.success(f"✅ Đã xóa {len(selected)} tài khoản")
                        st.rerun()
            else:
                st.info("Không có tài khoản nào để xóa (ngoài admin).")

    # ── Chuyển tài khoản (thay thế "Thử tài khoản" đã xóa khỏi sidebar) ──
    with st.expander("🔄 Chuyển tài khoản đăng nhập (dùng để kiểm tra phân quyền)"):
        st.caption("Chọn tài khoản để đăng nhập và xem app với quyền tương ứng.")
        switch_names = [u["Họ tên"] for u in st.session_state.users_list]
        cur_idx = next((i for i,u in enumerate(st.session_state.users_list) if u["Tài khoản"]==cu["Tài khoản"]), 0)
        sel_switch = st.selectbox("Chọn tài khoản:", switch_names, index=cur_idx, key="switch_user_sel")
        if st.button("✅ Chuyển sang tài khoản này", key="btn_switch_user"):
            for u in st.session_state.users_list:
                if u["Họ tên"] == sel_switch:
                    st.session_state.current_user = {"Tài khoản":u["Tài khoản"],"Họ tên":u["Họ tên"],"Vai trò":u["Phân quyền"]}
            st.rerun()

    st.write("")
    st.markdown("##### ✏️ Thao tác tài khoản")
    for i,u in enumerate(st.session_state.users_list):
        is_self  = u["Tài khoản"]==cu["Tài khoản"]
        is_admin_acc = u["Tài khoản"]=="admin"
        u_role   = u["Phân quyền"]

        # Quyền sửa thông tin & đổi mật khẩu
        can_edit = (role=="Quản lý") or is_self
        # Quyền xóa
        can_del = False
        if role=="Quản lý" and not is_admin_acc: can_del = True
        elif role=="Trưởng QC" and u_role=="Kiểm tra viên": can_del = True

        badge = "🔓" if (can_edit or can_del) else "🔒"
        with st.expander(f"{badge}  **{u['Họ tên']}** ({u['Tài khoản']}) — {u['Phân quyền']}"):
            if not can_edit and not can_del:
                st.caption("🔒 Không có quyền thao tác tài khoản này"); continue

            ca, cb, cc, _ = st.columns([2, 2, 2, 2])

            # ── Nút SỬA tài khoản ──────────────────────────
            if can_edit:
                with ca.popover("✏️ Sửa tài khoản"):
                    with st.form(f"frm_edit_user_{i}"):
                        st.markdown(f"**Sửa: {u['Họ tên']}**")
                        new_nm = st.text_input("Họ và tên", value=u["Họ tên"])
                        new_un = st.text_input("Tên tài khoản", value=u["Tài khoản"])
                        # Chỉ Admin mới đổi được phân quyền
                        if role == "Quản lý":
                            ro_opts = ["Quản lý","Trưởng QC","Kiểm tra viên"]
                            cur_ro  = u["Phân quyền"]
                            new_ro  = st.selectbox("Phân quyền", ro_opts,
                                        index=ro_opts.index(cur_ro) if cur_ro in ro_opts else 0)
                        else:
                            new_ro = u["Phân quyền"]
                            st.caption(f"Phân quyền: {new_ro}")
                        tt_opts = ["Hoạt động","Tạm khóa"]
                        cur_tt  = u.get("Trạng thái","Hoạt động")
                        new_tt  = st.selectbox("Trạng thái", tt_opts,
                                    index=tt_opts.index(cur_tt) if cur_tt in tt_opts else 0)
                        if st.form_submit_button("💾 Lưu thay đổi", use_container_width=True):
                            # Kiểm tra trùng tài khoản (nếu đổi tên TK)
                            if new_un != u["Tài khoản"] and any(
                                    x["Tài khoản"]==new_un for j,x in enumerate(st.session_state.users_list) if j!=i):
                                st.error("Tên tài khoản đã tồn tại!")
                            else:
                                st.session_state.users_list[i].update({
                                    "Họ tên": new_nm,
                                    "Tài khoản": new_un,
                                    "Phân quyền": new_ro,
                                    "Trạng thái": new_tt,
                                })
                                # Nếu đang sửa chính mình → cập nhật current_user
                                if is_self:
                                    st.session_state.current_user.update({
                                        "Tài khoản": new_un,
                                        "Họ tên": new_nm,
                                        "Vai trò": new_ro,
                                    })
                                ghi_log("Users","Sửa TK",f"Sửa {u['Tài khoản']} → {new_un}")
                                persist("users_list")
                                st.success("✅ Đã lưu!")
                                st.rerun()

            # ── Nút ĐỔI MẬT KHẨU ───────────────────────────
            if can_edit:
                with cb.popover("🔑 Đổi mật khẩu"):
                    with st.form(f"frm_pw_{i}"):
                        p1 = st.text_input("Mật khẩu mới", type="password")
                        p2 = st.text_input("Xác nhận lại", type="password")
                        if st.form_submit_button("✅ Xác nhận", use_container_width=True):
                            if not p1:
                                st.error("Mật khẩu không được trống!")
                            elif p1 != p2:
                                st.error("Mật khẩu xác nhận không khớp!")
                            else:
                                st.session_state.users_list[i]["Mật khẩu"] = p1
                                ghi_log("Users","Đổi pass",f"Đổi pass {u['Tài khoản']}")
                                persist("users_list")   # ← lưu ngay
                                st.success("✅ Đã đổi mật khẩu!")
                                st.rerun()

            # ── Nút XÓA tài khoản ───────────────────────────
            if can_del:
                with cc.popover("🗑️ Xóa"):
                    st.warning(f"Xác nhận xóa **{u['Họ tên']}**?")
                    if st.button("✅ Xác nhận xóa", key=f"confirm_del_{i}"):
                        st.session_state.users_list.pop(i)
                        ghi_log("Users","Xóa TK",f"Xóa {u['Tài khoản']}")
                        persist("users_list")
                        st.rerun()
