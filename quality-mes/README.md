# Quality MES - He thong Quan ly Chat luong Nha may San xuat

He thong quan ly chat luong toan dien cho nha may san xuat.

## Tinh nang

| Module | Mo ta |
|--------|-------|
| IQC | Kiem tra chat luong nguyen vat lieu dau vao |
| IPQC | Kiem tra chat luong trong qua trinh san xuat |
| OQC | Kiem tra chat luong san pham thanh pham |
| NCR + CAPA | Bao cao su khong phu hop & hanh dong khac phuc |
| SPC | Bao cao thong ke, bieu do kiem soat |
| Thiet bi do | Quan ly thiet bi do luong & lich hieu chuan |
| Nhat ky | Lich su hoat dong nguoi dung |

## Phien ban Web App (FastAPI + React)

### Cach chay local

```powershell
# Cua so 1 - Backend
cd backend
pip install -r requirements.txt
python deploy.py

# Cua so 2 - Frontend dev
cd frontend
npm install
npm run dev
```

Hoac deploy production (1 lenh):

```powershell
cd backend
python deploy.py
```

Truy cap: `http://localhost:8000`

### Tai khoan mac dinh

| Username | Password | Vai tro |
|----------|----------|---------|
| admin | Admin123 | Quan ly |
| qc_manager | Qc123456 | Truong QC |
| inspector1 | Insp123456 | Kiem tra vien |
| inspector2 | Insp123456 | Kiem tra vien |
| operator | Oper123456 | Cong nhan |

## Phien ban Streamlit Cloud

### Deploy len Streamlit Cloud

1. Push repo nay len GitHub
2. Vao [share.streamlit.io](https://share.streamlit.io)
3. New app -> Chon repo nay
4. Main file path: `quality-mes/streamlit_app.py`
5. Click Deploy!

### Chay local

```powershell
cd quality-mes
pip install streamlit plotly
pip install -r backend/requirements.txt
streamlit run streamlit_app.py
```

## Cong nghe

- **Backend**: Python FastAPI, SQLAlchemy, SQLite, JWT
- **Frontend**: React, TypeScript, Ant Design, Tailwind CSS, Recharts
- **Streamlit**: Python Streamlit, Plotly
