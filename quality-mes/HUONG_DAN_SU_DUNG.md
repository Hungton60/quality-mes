# Quality MES - HƯỚNG DẪN SỬ DỤNG

## He thong Quan ly Chat luong Nha may San xuat

---

## MUC LUC

1. [Cai dat va Chay ung dung](#1-cai-dat-va-chay-ung-dung)
2. [Dang nhap va Phan quyen](#2-dang-nhap-va-phan-quyen)
3. [Bang dieu khien (Dashboard)](#3-bang-dieu-khien-dashboard)
4. [IQC - Kiem tra dau vao](#4-iqc---kiem-tra-dau-vao)
5. [IPQC - Kiem tra qua trinh](#5-ipqc---kiem-tra-qua-trinh)
6. [OQC - Kiem tra thanh pham](#6-oqc---kiem-tra-thanh-pham)
7. [NCR + CAPA - Xu ly su khong phu hop](#7-ncr--capa---xu-ly-su-khong-phu-hop)
8. [SPC - Bao cao thong ke](#8-spc---bao-cao-thong-ke)
9. [Thiet bi do & Hieu chuan](#9-thiet-bi-do--hieu-chuan)
10. [Quan ly nguoi dung](#10-quan-ly-nguoi-dung)
11. [Nhat ky hoat dong](#11-nhat-ky-hoat-dong)
12. [Xuat bao cao Excel](#12-xuat-bao-cao-excel)
13. [Doi mat khau](#13-doi-mat-khau)
14. [Tich hop API](#14-tich-hop-api)

---

## 1. CAI DAT VA CHAY UNG DUNG

### Chay tren may ca nhan (Web App)

**Yeu cau:** Python 3.10+, Node.js 18+

```powershell
# Buoc 1: Cai thu vien Python
cd quality-mes\backend
pip install -r requirements.txt

# Buoc 2: Tao du lieu mau (neu chay lan dau)
python seed.py

# Buoc 3: Khoi dong may chu
python deploy.py
```

May chu se hien:
```
============================================================
  May chu:     http://192.168.1.5:8000
  Tai khoan mac dinh:
    admin / Admin123
============================================================
```

**Truy cap:** Mo trinh duyet, nhap `http://192.168.1.5:8000`

### Chay tren Streamlit Cloud (Online, mien phi)

1. Push code len GitHub
2. Vao https://share.streamlit.io
3. New app → Chon repo → File: `quality-mes/streamlit_app.py`
4. Deploy → Chia se link cho team

---

## 2. DANG NHAP VA PHAN QUYEN

### Tai khoan mac dinh

| Ten dang nhap | Mat khau | Vai tro | Quyen han |
|---------------|----------|---------|-----------|
| **admin** | Admin123 | Quan ly | Toan quyen he thong |
| **qc_manager** | Qc123456 | Truong QC | Xem + Tao phieu, NCR, bao cao |
| **inspector1** | Insp123456 | Kiem tra vien | Tao phieu kiem tra, nhap ket qua |
| **inspector2** | Insp123456 | Kiem tra vien | Tao phieu kiem tra, nhap ket qua |
| **operator** | Oper123456 | Cong nhan | Chi xem duoc ban than |

### Dang ky tai khoan moi

1. Tai trang dang nhap → Chon tab **Dang ky**
2. Nhap: Ho ten, Email, Ten dang nhap, Mat khau (toi thieu 6 ky tu)
3. Tai khoan moi mac dinh la **Kiem tra vien**
4. Admin co the doi vai tro sau

---

## 3. BANG DIEU KHIEN (DASHBOARD)

Trang chu hien thi tong quan he thong:

- **Tong phieu kiem tra:** Tong so phieu IQC + IPQC + OQC
- **Dat / Khong dat / Ty le dat:** Thong ke chat luong
- **NCR dang mo:** So su khong phu hop chua xu ly
- **NCR/CAPA qua han:** Canh bao cac viec tre han

Nhan vao cac **card module** de vao trang tuong ung.

Canh bao mau vang xuat hien khi co NCR hoac CAPA qua han.

---

## 4. IQC - KIEM TRA DAU VAO

Kiem tra chat luong **nguyen vat lieu** khi nhap ve tu nha cung cap.

### Quy trinh IQC

```
Buoc 1: Tao Nha cung cap → Buoc 2: Tao Nguyen lieu → Buoc 3: Tao Phieu kiem tra → Buoc 4: Nhap ket qua → Buoc 5: Ket luan Dat/Khong dat
```

### 4.1. Quan ly Nha cung cap (Tab NCC)

- Xem danh sach nha cung cap
- **Them NCC:** Nhap Ma NCC, Ten, Nguoi lien he, SDT, Email, Dia chi
- **Sua:** Nhan nut but chi → Sua thong tin → Luu
- **Xoa:** Nhan nut thung rac → Xac nhan

### 4.2. Quan ly Nguyen vat lieu (Tab Nguyen lieu)

- Xem danh sach nguyen lieu kem NCC
- **Them NL:** Nhap Ma NL, Ten, Dac tinh ky thuat, Don vi, Chon NCC
- **Import Excel:** Nhan nut Import Excel → Chon file `.xlsx`
  - File Excel can co cac cot: Ma, Ten, Dac tinh, Don vi, Supplier_ID

### 4.3. Tao phieu kiem tra IQC

1. Chon tab **Phieu kiem tra**
2. Nhan **Tao phieu kiem tra**
3. Nhap thong tin:
   - **So phieu:** VD: `IQC-2026-001`
   - **Nguyen lieu:** Chon tu danh sach
   - **Nha cung cap:** Chon tu danh sach
   - **So lo:** So lo cua nha cung cap
   - **So luong / Co mau:** Tong so luong lo hang va so luong lay mau
   - **Ngay kiem:** Ngay thuc hien kiem tra
   - **Nguoi kiem:** Chon nguoi kiem tra (dropdown)
4. Co the su dung **Bang AQL** de tinh co mau tu dong:
   - Chon muc kiem tra (G-I/G-II/G-III/S-1 den S-4)
   - Nhap kich thuoc lo → He thong tinh co mau tu dong

### 4.4. Nhap ket qua kiem tra

1. Nhan **Chi tiet** tren phieu can nhap
2. Nhan **Them ket qua**
3. Nhap tung muc kiem:
   - **Muc kiem:** Ten chi tieu (VD: Do day, Do rong, Do cung...)
   - **Tieu chuan:** Tieu chuan can dat
   - **Gia tri do:** Ket qua do thuc te
   - **Gioi han duoi / Gioi han tren:** Dung sai cho phep
   - **Ket qua:** Dat / Khong dat (tu dong neu nam trong dung sai)
4. Nhan **Them ket qua**

### 4.5. Ket luan phieu

Sau khi nhap du ket qua:
- Nhan **Dat** → Phieu chuyen trang thai Dat (Pass)
- Nhan **Khong dat** → Phieu chuyen trang thai Khong dat (Fail) → Co the tao NCR

---

## 5. IPQC - KIEM TRA QUA TRINH

Kiem tra chat luong **trong qua trinh san xuat** tai cac cong doan.

### Quy trinh IPQC

```
Buoc 1: Tao phieu IPQC → Buoc 2: Nhap ket qua do → Buoc 3: Ket luan Dat/Khong dat
```

### Tao phieu IPQC

1. Nhan **Tao phieu kiem tra**
2. Nhap thong tin:
   - **So phieu:** VD: `IPQC-2026-001`
   - **Cong doan:** Ten cong doan (VD: Han khung, Son tinh dien, Tien CNC...)
   - **Tram lam viec:** Vi tri tram (VD: Tram han 1, Line A...)
   - **May:** Ten may (VD: May han MIG-03, May tien CNC-01...)
   - **Ca:** Ca 1, Ca 2, hoac Ca 3
   - **Co mau:** So mau lay de kiem tra (thuong 5 san pham)
   - **Ngay kiem / Nguoi kiem**
3. Nhan **Tao phieu**

### Nhap ket qua IPQC

Tuong tu IQC: Nhan **Chi tiet** → **Them ket qua** → Nhap gia tri do → Ket luan

---

## 6. OQC - KIEM TRA THANH PHAM

Kiem tra chat luong **san pham cuoi cung** truoc khi xuat hang.

### Quy trinh OQC

```
Buoc 1: Tao San pham → Buoc 2: Tao phieu OQC → Buoc 3: Nhap ket qua → Buoc 4: Ket luan
```

### 6.1. Quan ly San pham (Tab San pham)

- Xem danh sach san pham
- **Them SP:** Ma SP, Ten SP, Dac tinh, Don vi
- **Import Excel:** Nhan Import Excel → Chon file `.xlsx`
  - File Excel can co cac cot: Ma, Ten, Dac tinh, Don vi

### 6.2. Tao phieu OQC

1. Chon tab **Phieu kiem tra**
2. Nhan **Tao phieu kiem tra**
3. Nhap: So phieu, San pham, So lo, So luong, Co mau, Ngay kiem, Nguoi kiem
4. Nhap ket qua va ket luan Dat/Khong dat

---

## 7. NCR + CAPA - XU LY SU KHONG PHU HOP

Quy trinh xu ly khi phat hien loi / khong phu hop.

### Luong xu ly

```
Phat hien loi → Tao NCR → Dieu tra → Tao CAPA → Thuc hien → Hoan thanh → Xac nhan → Dong NCR
   (Mo)        (Dang dieu tra)          (Dang thuc hien)  (Hoan thanh)  (Da xac nhan)  (Dong)
```

### 7.1. Tao NCR (Bao cao su khong phu hop)

1. Chon tab **NCR**
2. Nhan **Tao NCR moi**
3. Nhap thong tin:
   - **So NCR:** VD: `NCR-2026-001`
   - **Tieu de:** Mo ta ngan gon van de
   - **Mo ta chi tiet:** Mo ta day du ve loi
   - **Muc do:**
     - *Nghiem trong (Critical):* Anh huong an toan hoac chuc nang san pham
     - *Lon (Major):* Anh huong dang ke den chat luong
     - *Nho (Minor):* Sai lech nho, khong anh huong chuc nang
   - **Nguon phat hien:** IQC, IPQC, OQC, hoac Khac
   - **Nguoi bao cao / Nguoi xu ly**
   - **Han xu ly:** Ngay can hoan thanh

### 7.2. Xu ly NCR

Chuyen trang thai NCR qua cac buoc:
- **Dieu tra:** Dang tim nguyen nhan
- **Da xu ly:** Da co giai phap
- **Dong:** Da hoan tat

### 7.3. Tao CAPA (Hanh dong khac phuc/phong ngua)

Trong chi tiet NCR, nhan **Them CAPA**:
- **So CAPA:** VD: `CAPA-2026-001`
- **Tieu de:** Ten hanh dong
- **Loai:**
  - *Khac phuc (Corrective):* Sua loi da xay ra
  - *Phong ngua (Preventive):* Ngan loi xay ra trong tuong lai
- **Nguyen nhan goc:** Phan tich 5 Why, bieaudo xuong ca...
- **Ke hoach hanh dong:** Cac buoc cu the
- **Nguoi phu trach / Han hoan thanh**

### 7.4. Theo doi CAPA

Chuyen trang thai CAPA:
- **Dang thuc hien** → **Hoan thanh** → **Da xac nhan**

### 7.5. Xem tong hop CAPA

Tab **CAPA** hien thi danh sach tat ca CAPA, co the loc theo trang thai.

---

## 8. SPC - BAO CAO THONG KE

### 8.1. Tong quan

Trang SPC hien thi:
- **Bang tong hop:** Tong so phieu IQC, IPQC, OQC
- **Ty le dat** cho tung module

### 8.2. Bieu do kiem soat (X-bar Chart)

- Hien thi gia tri trung binh cho tung muc kiem
- So sanh voi gioi han duoi (LCL) va gioi han tren (UCL)

### 8.3. Bieu do Histogram

- Hien thi phan bo tan suat cac gia tri do
- Nhan biet phan bo co trong dung sai hay khong

### 8.4. Bieu do Pareto

- Xem cac loi thuong gap nhat
- Chon module (IQC/OQC/IPQC)
- Hien thi thu tu loi tu nhieu → it

### 8.5. Xu huong theo thoi gian

- Xem xu huong gia tri do theo thoi gian
- Duong LCL/UCL de phat hien diem bat thuong

---

## 9. THIET BI DO & HIEU CHUAN

### 9.1. Them thiet bi do

1. Vao trang **Thiet bi do**
2. Nhan **Them thiet bi**
3. Nhap thong tin:
   - **Ma thiet bi:** VD: `TB-001`
   - **Ten thiet bi:** VD: `Thuoc cap dien tu Mitutoyo 0-150mm`
   - **Loai:** Do luong, Thu nghiem, Dung cu kiem, Khac
   - **So serie:** So serie cua nha san xuat
   - **Vi tri:** Vi tri dat thiet bi
   - **Chu ky hieu chuan:** So ngay giua 2 lan hieu chuan (thuong 365 ngay)
   - **Ngay hieu chuan gan nhat**

### 9.2. Theo doi hieu chuan

Bang thiet bi hien thi:
- **Den xanh:** Con han hieu chuan
- **Den cam:** Sap den han (<= 30 ngay)
- **Den do:** DA QUA HAN hieu chuan
- So ngay con lai / so ngay qua han

### 9.3. Hieu chuan thiet bi

1. Nhan nut **Hieu chuan**
2. Chon ngay hieu chuan
3. Nhan **Xac nhan** → He thong tu dong tinh han hieu chuan tiep theo

---

## 10. QUAN LY NGUOI DUNG

*(Danh cho tien)*

### 10.1. Xem danh sach nguoi dung

Vao trang **Nguoi dung** → Xem tat ca tai khoan

### 10.2. Them nguoi dung moi

1. Nhan **Them nguoi dung**
2. Nhap: Ten dang nhap, Email, Ho ten, Mat khau, Vai tro
3. Nhan **Tao nguoi dung**

### 10.3. Sua nguoi dung

1. Nhan nut but chi tren nguoi dung can sua
2. Co the doi: **Vai tro** va **Trang thai hoat dong**
3. Nhan **Cap nhat**

### 10.4. Xoa / Vo hieu nguoi dung

- **Xoa:** Nhan thung rac → Xac nhan (xoa vinh vien)
- **Vo hieu:** Sua → Tat Switch "Hoat dong" → Nguoi dung khong the dang nhap

### Cac vai tro

| Vai tro | Quyen han |
|---------|-----------|
| Quan ly (admin) | Toan quyen: xem, tao, sua, xoa tat ca. Quan ly nguoi dung |
| Truong QC (qc_manager) | Xem + Tao phieu, NCR, CAPA, bao cao. Khong quan ly nguoi dung |
| Kiem tra vien (inspector) | Tao phieu kiem tra, nhap ket qua. Xem du lieu |
| Cong nhan (operator) | Chi xem duoc ban than, khong tao/sua duoc |

---

## 11. NHAT KY HOAT DONG

Trang **Nhat ky** ghi lai moi thao tac trong he thong:

- **Thoi gian:** Khi nao
- **Nguoi dung:** Ai thuc hien
- **Hanh dong:** Tao / Sua / Xoa / Hieu chuan / Dang nhap
- **Module:** IQC, OQC, IPQC, NCR, CAPA, Thiet bi...
- **Mo ta:** Chi tiet hanh dong

Co the **loc theo module** de xem nhat ky cua tung phan he.

---

## 12. XUAT BAO CAO EXCEL

### Xuat danh sach phieu kiem tra

1. Vao trang IQC, IPQC, hoac OQC
2. Nhan nut **Xuat Excel**
3. File Excel duoc tai ve voi cac cot:
   - So phieu, Trang thai, Ngay kiem, Nguoi kiem, Ghi chu

### Import du lieu tu Excel

**Nguyen lieu:**
1. Vao IQC → Tab Nguyen lieu → Nhan **Import Excel**
2. Chon file `.xlsx` dinh dang:
   - Cot A: Ma NL, Cot B: Ten NL, Cot C: Dac tinh, Cot D: Don vi, Cot E: Supplier_ID

**San pham:**
1. Vao OQC → Tab San pham → Nhan **Import Excel**
2. Chon file `.xlsx` dinh dang:
   - Cot A: Ma SP, Cot B: Ten SP, Cot C: Dac tinh, Cot D: Don vi

---

## 13. DOI MAT KHAU

1. Nhan vao **ten nguoi dung** o goc phai man hinh
2. Chon **Doi mat khau**
3. Nhap: Mat khau cu + Mat khau moi (toi thieu 6 ky tu)
4. Nhan **Doi mat khau**

---

## 14. TICH HOP API

Quality MES cung cap **REST API** de tich hop voi cac he thong khac (ERP, MES, SCADA, BI...).

### 14.1. Truy cap tai lieu API

Mo trinh duyet: `http://192.168.1.5:8000/api/docs`

Giao dien Swagger UI cho phep test truc tiep moi API.

### 14.2. Xac thuc API

Tat ca API (tru dang nhap/dang ky) can gui kem JWT token trong header:

```
Authorization: Bearer <token>
```

**Lay token:**
```
POST /api/auth/login
Body: {"username": "admin", "password": "Admin123"}
Response: {"access_token": "eyJ...", "token_type": "bearer", "user": {...}}
```

### 14.3. Vi du tich hop

**Python:**
```python
import requests

BASE = "http://192.168.1.5:8000"

# Dang nhap
r = requests.post(f"{BASE}/api/auth/login",
    json={"username": "admin", "password": "Admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Tao phieu IQC
requests.post(f"{BASE}/api/iqc/inspections", headers=headers, json={
    "inspection_no": "IQC-2026-050",
    "material_id": 1,
    "supplier_id": 1,
    "lot_no": "LOT-ABC-001",
    "quantity": 10000,
    "sample_size": 80,
    "inspection_date": "2026-05-25T08:00:00",
    "inspector_id": 1
})

# Lay thong ke chat luong
stats = requests.get(f"{BASE}/api/spc/summary", headers=headers).json()
print(f"IQC: {stats['iqc']['total']} phieu, Dat: {stats['iqc']['pass']}")

# Kiem tra NCR qua han
overdue = requests.get(f"{BASE}/api/overdue", headers=headers).json()
print(f"NCR qua han: {overdue['overdue_ncrs']}")
```

**JavaScript (Node.js):**
```javascript
const BASE = "http://192.168.1.5:8000";

// Dang nhap
const loginRes = await fetch(`${BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: "admin", password: "Admin123" })
});
const { access_token } = await loginRes.json();

// Goi API
const res = await fetch(`${BASE}/api/iqc/inspections`, {
    headers: { Authorization: `Bearer ${access_token}` }
});
const inspections = await res.json();
```

### 14.4. Danh sach API endpoints

| Method | URL | Mo ta |
|--------|-----|-------|
| POST | `/api/auth/login` | Dang nhap, lay token |
| POST | `/api/auth/register` | Dang ky tai khoan |
| GET | `/api/auth/me` | Thong tin nguoi dung hien tai |
| GET | `/api/iqc/suppliers` | Danh sach nha cung cap |
| POST | `/api/iqc/suppliers` | Them nha cung cap |
| GET | `/api/iqc/materials` | Danh sach nguyen lieu |
| POST | `/api/iqc/materials` | Them nguyen lieu |
| GET | `/api/iqc/inspections` | Danh sach phieu IQC |
| POST | `/api/iqc/inspections` | Tao phieu IQC |
| POST | `/api/iqc/inspections/{id}/results` | Them ket qua IQC |
| PUT | `/api/iqc/inspections/{id}/status` | Cap nhat trang thai IQC |
| GET | `/api/oqc/products` | Danh sach san pham |
| POST | `/api/oqc/products` | Them san pham |
| GET | `/api/oqc/inspections` | Danh sach phieu OQC |
| POST | `/api/oqc/inspections` | Tao phieu OQC |
| GET | `/api/ipqc/inspections` | Danh sach phieu IPQC |
| POST | `/api/ipqc/inspections` | Tao phieu IPQC |
| GET | `/api/ncr/` | Danh sach NCR |
| POST | `/api/ncr/` | Tao NCR |
| GET | `/api/ncr/{id}` | Chi tiet NCR |
| PUT | `/api/ncr/{id}/status` | Cap nhat trang thai NCR |
| POST | `/api/ncr/{id}/capas` | Them CAPA cho NCR |
| GET | `/api/spc/summary` | Thong ke tong quan |
| GET | `/api/spc/pareto/iqc` | Pareto IQC |
| GET | `/api/spc/pareto/oqc` | Pareto OQC |
| GET | `/api/spc/results/{module}` | Du lieu do luong |
| GET | `/api/overdue` | NCR/CAPA qua han |
| GET | `/api/equipment/` | Danh sach thiet bi |
| POST | `/api/equipment/` | Them thiet bi |
| PUT | `/api/equipment/{id}/calibrate` | Hieu chuan thiet bi |
| GET | `/api/export/inspections` | Xuat Excel phieu kiem tra |
| POST | `/api/import/materials` | Import Excel nguyen lieu |
| POST | `/api/import/products` | Import Excel san pham |
| GET | `/api/users/` | Danh sach nguoi dung (admin) |
| POST | `/api/users/` | Them nguoi dung (admin) |
| PUT | `/api/users/{id}` | Sua nguoi dung (admin) |
| GET | `/api/users/lookup` | Tim nguoi dung (dropdown) |
| GET | `/api/activity-logs` | Nhat ky hoat dong |
| POST | `/api/change-password` | Doi mat khau |
| GET | `/api/aql-table` | Bang tra AQL |

### 14.5. Tich hop database truc tiep

Co the ket noi truc tiep den database SQLite de doc du lieu:

**Power BI / Excel:**
1. Get Data → ODBC → SQLite
2. Chon file `quality_mes.db`

**Grafana:**
1. Cai SQLite datasource plugin
2. Ket noi den `quality_mes.db`
3. Tao dashboard tu cac bang: `iqc_inspections`, `oqc_inspections`, `ncrs`, `capas`...

**Python script:**
```python
import sqlite3
conn = sqlite3.connect("quality_mes.db")
df = pd.read_sql("SELECT * FROM iqc_inspections", conn)
```

---

## PHU LUC: CACH KHOI PHUC DU LIEU

### Reset toan bo du lieu

```powershell
cd quality-mes\backend
# Xoa database cu
del quality_mes.db
# Tao lai du lieu mau
python seed.py
python deploy.py
```

### Sao luu du lieu

```powershell
# Copy file database
copy quality-mes\backend\quality_mes.db D:\Backup\quality_mes_backup.db
```

---

## HO TRO

- **API Docs:** `http://dia-chi-may:8000/api/docs`
- **GitHub Issues:** Tao issue tren repo GitHub
- **Lien he:** Bo phan IT / Quan ly he thong

---

*Quality MES v1.0 - Tai lieu cap nhat 05/2026*
