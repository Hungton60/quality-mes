# Quality MES - HƯỚNG DẪN SỬ DỤNG

## Hệ thống Quản lý Chất lượng Nhà máy Sản xuất

---

## MỤC LỤC

1. [Cài đặt và Chạy ứng dụng](#1-cài-đặt-và-chạy-ứng-dụng)
2. [Đăng nhập và Phân quyền](#2-đăng-nhập-và-phân-quyền)
3. [Bảng điều khiển (Dashboard)](#3-bảng-điều-khiển-dashboard)
4. [IQC - Kiểm tra đầu vào](#4-iqc---kiểm-tra-đầu-vào)
5. [IPQC - Kiểm tra quá trình](#5-ipqc---kiểm-tra-quá-trình)
6. [OQC - Kiểm tra thành phẩm](#6-oqc---kiểm-tra-thành-phẩm)
7. [NCR + CAPA - Xử lý sự không phù hợp](#7-ncr--capa---xử-lý-sự-không-phù-hợp)
8. [Checklist mẫu - Tự động điền mục kiểm](#8-checklist-mẫu---tự-động-điền-mục-kiểm)
9. [SPC - Báo cáo thống kê](#9-spc---báo-cáo-thống-kê)
10. [Thiết bị đo & Hiệu chuẩn](#10-thiết-bị-đo--hiệu-chuẩn)
11. [Quản lý người dùng](#11-quản-lý-người-dùng)
12. [Nhật ký hoạt động](#12-nhật-ký-hoạt-động)
13. [Xuất báo cáo Excel](#13-xuất-báo-cáo-excel)
14. [Đổi mật khẩu](#14-đổi-mật-khẩu)
15. [Cài đặt PWA (App điện thoại)](#15-cài-đặt-pwa-app-điện-thoại)
16. [Deploy online 24/7 (Render)](#16-deploy-online-247-render)
17. [Tích hợp API](#17-tích-hợp-api)

---

## 1. CÀI ĐẶT VÀ CHẠY ỨNG DỤNG

### Cách 1: Truy cập Online (Render - miễn phí 24/7)

Không cần cài đặt gì. Mở trình duyệt, vào link:
```
https://quality-mes-xxx.onrender.com
```
*(Link được cấp khi deploy, xem chương 16)*

Tài khoản mặc định: `admin` / `Admin123`

### Cách 2: Chạy trên máy cá nhân (Web App)

**Yêu cầu:** Python 3.10+, Node.js 18+

*Bước 1: Cài thư viện Python*
```powershell
cd quality-mes\backend
pip install -r requirements.txt
```

*Bước 2: Tạo dữ liệu mẫu (nếu chạy lần đầu)*
```powershell
python seed.py
```

*Bước 3: Khởi động máy chủ*
```powershell
python deploy.py
```

Máy chủ hiển thị địa chỉ IP để truy cập trong mạng LAN.

### Cách 3: Streamlit (Online đơn giản)

1. Vào https://share.streamlit.io
2. Deploy từ repo GitHub
3. Giao diện đơn giản, dùng được ngay không cần cài đặt

---

## 2. ĐĂNG NHẬP VÀ PHÂN QUYỀN

### Tài khoản mặc định

| Tên đăng nhập | Mật khẩu | Vai trò | Quyền hạn |
|---------------|----------|---------|-----------|
| **admin** | Admin123 | Quản lý | Toàn quyền hệ thống |
| **qc_manager** | Qc123456 | Trưởng QC | Xem + Tạo phiếu, NCR, báo cáo |
| **inspector1** | Insp123456 | Kiểm tra viên | Tạo phiếu kiểm tra, nhập kết quả |
| **inspector2** | Insp123456 | Kiểm tra viên | Tạo phiếu kiểm tra, nhập kết quả |
| **operator** | Oper123456 | Công nhân | Chỉ xem được bản thân |

### Đăng ký tài khoản mới

1. Tại trang đăng nhập → Chọn tab **Đăng ký**
2. Nhập: Họ tên, Email, Tên đăng nhập, Mật khẩu (tối thiểu 6 ký tự)
3. Tự đăng ký chỉ được vai trò **inspector** hoặc **operator**
4. Muốn làm **qc_manager** hoặc **admin**: phải nhờ admin tạo tài khoản

### Ai có quyền tạo tài khoản?

| Cách tạo | Vai trò được phép |
|----------|-------------------|
| Tự đăng ký (tab Đăng ký) | inspector, operator |
| Admin tạo (menu Người dùng) | admin, qc_manager, inspector, operator |

Chỉ **admin** mới vào được menu **Người dùng** để tạo/sửa/xóa tài khoản.

---

## 3. BẢNG ĐIỀU KHIỂN (DASHBOARD)

Trang chủ hiển thị tổng quan hệ thống:

- **Tổng phiếu kiểm tra:** Tổng số phiếu IQC + IPQC + OQC
- **Đạt / Không đạt / Tỷ lệ đạt:** Thống kê chất lượng
- **NCR đang mở:** Số sự không phù hợp chưa xử lý
- **NCR/CAPA quá hạn:** Cảnh báo các việc trễ hạn

Nhấn vào các **card module** để vào trang tương ứng.

Cảnh báo màu vàng xuất hiện khi có NCR hoặc CAPA quá hạn.

---

## 4. IQC - KIỂM TRA ĐẦU VÀO

Kiểm tra chất lượng **nguyên vật liệu** khi nhập về từ nhà cung cấp.

### Quy trình IQC

```
Bước 1: Tạo Nhà cung cấp → Bước 2: Tạo Nguyên liệu → Bước 3: Tạo Phiếu kiểm tra → Bước 4: Nhập kết quả → Bước 5: Kết luận Đạt/Không đạt
```

### 4.1. Quản lý Nhà cung cấp (Tab NCC)

- Xem danh sách nhà cung cấp
- **Thêm NCC:** Nhập Mã NCC, Tên, Người liên hệ, SĐT, Email, Địa chỉ
- **Sửa:** Nhấn nút bút chì → Sửa thông tin → Lưu
- **Xóa:** Nhấn nút thùng rác → Xác nhận

### 4.2. Quản lý Nguyên vật liệu (Tab Nguyên liệu)

- Xem danh sách nguyên liệu kèm NCC
- **Thêm NL:** Nhập Mã NL, Tên, Đặc tính kỹ thuật, Đơn vị, Chọn NCC
- **Import Excel:** Nhấn nút Import Excel → Chọn file `.xlsx`
  - File Excel cần có các cột: Mã, Tên, Đặc tính, Đơn vị, Supplier_ID

### 4.3. Tạo phiếu kiểm tra IQC

1. Chọn tab **Phiếu kiểm tra**
2. Nhấn **Tạo phiếu kiểm tra**
3. Nhập thông tin:
   - **Số phiếu:** VD: `IQC-2026-001`
   - **Nguyên liệu:** Chọn từ danh sách
   - **Nhà cung cấp:** Chọn từ danh sách
   - **Số lô:** Số lô của nhà cung cấp
   - **Số lượng / Cỡ mẫu:** Tổng số lượng lô hàng và số lượng lấy mẫu
   - **Ngày kiểm:** Ngày thực hiện kiểm tra
   - **Người kiểm:** Chọn người kiểm tra (dropdown)
4. Có thể sử dụng **Bảng AQL** để tính cỡ mẫu tự động:
   - Chọn mức kiểm tra (G-I/G-II/G-III/S-1 đến S-4)
   - Nhập kích thước lô → Hệ thống tính cỡ mẫu tự động

### 4.4. Nhập kết quả kiểm tra

1. Nhấn **Chi tiết** trên phiếu cần nhập
2. Nhấn **Thêm kết quả**
3. Nhập từng mục kiểm:
   - **Mục kiểm:** Tên chỉ tiêu (VD: Độ dày, Độ rộng, Độ cứng...)
   - **Tiêu chuẩn:** Tiêu chuẩn cần đạt
   - **Giá trị đo:** Kết quả đo thực tế
   - **Giới hạn dưới / Giới hạn trên:** Dung sai cho phép
   - **Kết quả:** Đạt / Không đạt (tự động nếu nằm trong dung sai)
4. Nhấn **Thêm kết quả**

### 4.5. Kết luận phiếu

Sau khi nhập đủ kết quả:
- Nhấn **Đạt** → Phiếu chuyển trạng thái Đạt (Pass)
- Nhấn **Không đạt** → Phiếu chuyển trạng thái Không đạt (Fail) → Có thể tạo NCR

---

## 5. IPQC - KIỂM TRA QUÁ TRÌNH

Kiểm tra chất lượng **trong quá trình sản xuất** tại các công đoạn.

### Quy trình IPQC

```
Bước 1: Tạo phiếu IPQC → Bước 2: Nhập kết quả đo → Bước 3: Kết luận Đạt/Không đạt
```

### Tạo phiếu IPQC

1. Nhấn **Tạo phiếu kiểm tra**
2. Nhập thông tin:
   - **Số phiếu:** VD: `IPQC-2026-001`
   - **Công đoạn:** Tên công đoạn (VD: Hàn khung, Sơn tĩnh điện, Tiện CNC...)
   - **Trạm làm việc:** Vị trí trạm (VD: Trạm hàn 1, Line A...)
   - **Máy:** Tên máy (VD: Máy hàn MIG-03, Máy tiện CNC-01...)
   - **Ca:** Ca 1, Ca 2, hoặc Ca 3
   - **Cỡ mẫu:** Số mẫu lấy để kiểm tra (thường 5 sản phẩm)
   - **Ngày kiểm / Người kiểm**
3. Nhấn **Tạo phiếu**

### Nhập kết quả IPQC

Tương tự IQC: Nhấn **Chi tiết** → **Thêm kết quả** → Nhập giá trị đo → Kết luận

---

## 6. OQC - KIỂM TRA THÀNH PHẨM

Kiểm tra chất lượng **sản phẩm cuối cùng** trước khi xuất hàng.

### Quy trình OQC

```
Bước 1: Tạo Sản phẩm → Bước 2: Tạo phiếu OQC → Bước 3: Nhập kết quả → Bước 4: Kết luận
```

### 6.1. Quản lý Sản phẩm (Tab Sản phẩm)

- Xem danh sách sản phẩm
- **Thêm SP:** Mã SP, Tên SP, Đặc tính, Đơn vị
- **Import Excel:** Nhấn Import Excel → Chọn file `.xlsx`
  - File Excel cần có các cột: Mã, Tên, Đặc tính, Đơn vị

### 6.2. Tạo phiếu OQC

1. Chọn tab **Phiếu kiểm tra**
2. Nhấn **Tạo phiếu kiểm tra**
3. Nhập: Số phiếu, Sản phẩm, Số lô, Số lượng, Cỡ mẫu, Ngày kiểm, Người kiểm
4. Nhập kết quả và kết luận Đạt/Không đạt

---

## 7. NCR + CAPA - XỬ LÝ SỰ KHÔNG PHÙ HỢP

Quy trình xử lý khi phát hiện lỗi / không phù hợp.

### Luồng xử lý

```
Phát hiện lỗi → Tạo NCR → Điều tra → Tạo CAPA → Thực hiện → Hoàn thành → Xác nhận → Đóng NCR
   (Mở)        (Đang điều tra)          (Đang thực hiện)  (Hoàn thành)  (Đã xác nhận)  (Đóng)
```

### 7.1. Tạo NCR (Báo cáo sự không phù hợp)

1. Chọn tab **NCR**
2. Nhấn **Tạo NCR mới**
3. Nhập thông tin:
   - **Số NCR:** VD: `NCR-2026-001`
   - **Tiêu đề:** Mô tả ngắn gọn vấn đề
   - **Mô tả chi tiết:** Mô tả đầy đủ về lỗi
   - **Mức độ:**
     - *Nghiêm trọng (Critical):* Ảnh hưởng an toàn hoặc chức năng sản phẩm
     - *Lớn (Major):* Ảnh hưởng đáng kể đến chất lượng
     - *Nhỏ (Minor):* Sai lệch nhỏ, không ảnh hưởng chức năng
   - **Nguồn phát hiện:** IQC, IPQC, OQC, hoặc Khác
   - **Người báo cáo / Người xử lý**
   - **Hạn xử lý:** Ngày cần hoàn thành

### 7.2. Xử lý NCR

Chuyển trạng thái NCR qua các bước:
- **Điều tra:** Đang tìm nguyên nhân
- **Đã xử lý:** Đã có giải pháp
- **Đóng:** Đã hoàn tất

### 7.3. Tạo CAPA (Hành động khắc phục/phòng ngừa)

Trong chi tiết NCR, nhấn **Thêm CAPA**:
- **Số CAPA:** VD: `CAPA-2026-001`
- **Tiêu đề:** Tên hành động
- **Loại:**
  - *Khắc phục (Corrective):* Sửa lỗi đã xảy ra
  - *Phòng ngừa (Preventive):* Ngăn lỗi xảy ra trong tương lai
- **Nguyên nhân gốc:** Phân tích 5 Why, biểu đồ xương cá...
- **Kế hoạch hành động:** Các bước cụ thể
- **Người phụ trách / Hạn hoàn thành**

### 7.4. Theo dõi CAPA

Chuyển trạng thái CAPA:
- **Đang thực hiện** → **Hoàn thành** → **Đã xác nhận**

### 7.5. Xem tổng hợp CAPA

Tab **CAPA** hiển thị danh sách tất cả CAPA, có thể lọc theo trạng thái.

---

## 8. CHECKLIST MẪU - TỰ ĐỘNG ĐIỀN MỤC KIỂM

Tính năng giúp tạo **mẫu checklist** có sẵn, khi tạo phiếu kiểm tra chỉ cần chọn checklist → hệ thống tự động điền tất cả mục kiểm.

### 8.1. Tạo checklist mới (thủ công)

1. Vào menu **Checklist mẫu** (bên trái)
2. Nhấn **Tạo checklist mới**
3. Nhập:
   - **Mã checklist:** VD: `IQC-THEP`
   - **Tên checklist:** VD: `Kiểm tra thép tấm 2mm`
   - **Module:** IQC, OQC, hoặc IPQC
4. Thêm từng mục kiểm:
   - **Mục kiểm:** Tên chỉ tiêu (Độ dày, Độ rộng...)
   - **Tiêu chuẩn:** Mô tả tiêu chuẩn
   - **Min / Max:** Giới hạn dung sai
5. Nhấn dấu `+` để thêm nhiều mục → Nhấn **Tạo mới**

### 8.2. Import checklist từ file Excel (.xlsx)

1. Chuẩn bị file Excel, mỗi **sheet** = 1 checklist. Tên sheet = Mã checklist
2. Cột: Mục kiểm | Tiêu chuẩn | Min | Max

Ví dụ:
```
Sheet: "IQC-THEP-2MM"
| Mục kiểm     | Tiêu chuẩn    | Min  | Max  |
| Độ dày       | 2.0mm +/-0.1  | 1.9  | 2.1  |
| Độ rộng      | 1200mm +/-2   | 1198 | 1202 |
```

3. Vào **Checklist mẫu** → Chọn module → Nhấn **Import Excel** → Chọn file

### 8.3. Import checklist từ file Word (.docx)

1. Chuẩn bị file Word, mỗi **bảng (table)** = 1 checklist
2. Cột: Mục kiểm | Tiêu chuẩn | Min | Max
3. Dòng tiêu đề tự động bỏ qua
4. Vào **Checklist mẫu** → Nhấn **Import Excel** → Chọn file `.docx`

### 8.4. Sử dụng checklist khi tạo phiếu

1. Vào IQC/OQC/IPQC → **Tạo phiếu kiểm tra**
2. Điền thông tin phiếu → Chọn **Checklist mẫu** từ dropdown
3. Nhấn **Tạo phiếu** → Hệ thống tự động tạo sẵn các mục kiểm
4. Chỉ cần nhập **giá trị đo thực tế** cho từng mục

---

## 9. SPC - BÁO CÁO THỐNG KÊ

### 9.1. Tổng quan

Trang SPC hiển thị:
- **Bảng tổng hợp:** Tổng số phiếu IQC, IPQC, OQC
- **Tỷ lệ đạt** cho từng module

### 9.2. Biểu đồ kiểm soát (X-bar Chart)

- Hiển thị giá trị trung bình cho từng mục kiểm
- So sánh với giới hạn dưới (LCL) và giới hạn trên (UCL)

### 9.3. Biểu đồ Histogram

- Hiển thị phân bố tần suất các giá trị đo
- Nhận biết phân bố có trong dung sai hay không

### 9.4. Biểu đồ Pareto

- Xem các lỗi thường gặp nhất
- Chọn module (IQC/OQC/IPQC)
- Hiển thị thứ tự lỗi từ nhiều → ít

### 9.5. Xu hướng theo thời gian

- Xem xu hướng giá trị đo theo thời gian
- Đường LCL/UCL để phát hiện điểm bất thường

---

## 10. THIẾT BỊ ĐO & HIỆU CHUẨN

### 10.1. Thêm thiết bị đo

1. Vào trang **Thiết bị đo**
2. Nhấn **Thêm thiết bị**
3. Nhập thông tin:
   - **Mã thiết bị:** VD: `TB-001`
   - **Tên thiết bị:** VD: `Thước cặp điện tử Mitutoyo 0-150mm`
   - **Loại:** Đo lường, Thử nghiệm, Dụng cụ kiểm, Khác
   - **Số serie:** Số serie của nhà sản xuất
   - **Vị trí:** Vị trí đặt thiết bị
   - **Chu kỳ hiệu chuẩn:** Số ngày giữa 2 lần hiệu chuẩn (thường 365 ngày)
   - **Ngày hiệu chuẩn gần nhất**

### 10.2. Theo dõi hiệu chuẩn

Bảng thiết bị hiển thị:
- **Đèn xanh:** Còn hạn hiệu chuẩn
- **Đèn cam:** Sắp đến hạn (<= 30 ngày)
- **Đèn đỏ:** ĐÃ QUÁ HẠN hiệu chuẩn
- Số ngày còn lại / số ngày quá hạn

### 10.3. Hiệu chuẩn thiết bị

1. Nhấn nút **Hiệu chuẩn**
2. Chọn ngày hiệu chuẩn
3. Nhấn **Xác nhận** → Hệ thống tự động tính hạn hiệu chuẩn tiếp theo

---

## 11. QUẢN LÝ NGƯỜI DÙNG

*(Dành cho admin)*

### 11.1. Xem danh sách người dùng

Vào trang **Người dùng** → Xem tất cả tài khoản

### 11.2. Thêm người dùng mới

1. Nhấn **Thêm người dùng**
2. Nhập: Tên đăng nhập, Email, Họ tên, Mật khẩu, Vai trò
3. Nhấn **Tạo người dùng**

### 11.3. Sửa người dùng

1. Nhấn nút bút chì trên người dùng cần sửa
2. Có thể đổi: **Vai trò** và **Trạng thái hoạt động**
3. Nhấn **Cập nhật**

### 11.4. Xóa / Vô hiệu người dùng

- **Xóa:** Nhấn thùng rác → Xác nhận (xóa vĩnh viễn)
- **Vô hiệu:** Sửa → Tắt Switch "Hoạt động" → Người dùng không thể đăng nhập

### Các vai trò

| Vai trò | Quyền hạn |
|---------|-----------|
| Quản lý (admin) | Toàn quyền: xem, tạo, sửa, xóa tất cả. Quản lý người dùng |
| Trưởng QC (qc_manager) | Xem + Tạo phiếu, NCR, CAPA, báo cáo. Không quản lý người dùng |
| Kiểm tra viên (inspector) | Tạo phiếu kiểm tra, nhập kết quả. Xem dữ liệu |
| Công nhân (operator) | Chỉ xem được bản thân, không tạo/sửa được |

---

## 12. NHẬT KÝ HOẠT ĐỘNG

Trang **Nhật ký** ghi lại mọi thao tác trong hệ thống:

- **Thời gian:** Khi nào
- **Người dùng:** Ai thực hiện
- **Hành động:** Tạo / Sửa / Xóa / Hiệu chuẩn / Đăng nhập
- **Module:** IQC, OQC, IPQC, NCR, CAPA, Thiết bị...
- **Mô tả:** Chi tiết hành động

Có thể **lọc theo module** để xem nhật ký của từng phân hệ.

---

## 13. XUẤT BÁO CÁO EXCEL

### Xuất danh sách phiếu kiểm tra

1. Vào trang IQC, IPQC, hoặc OQC
2. Nhấn nút **Xuất Excel**
3. File Excel được tải về với các cột:
   - Số phiếu, Trạng thái, Ngày kiểm, Người kiểm, Ghi chú

### Import dữ liệu từ Excel

**Nguyên liệu:**
1. Vào IQC → Tab Nguyên liệu → Nhấn **Import Excel**
2. Chọn file `.xlsx` định dạng:
   - Cột A: Mã NL, Cột B: Tên NL, Cột C: Đặc tính, Cột D: Đơn vị, Cột E: Supplier_ID

**Sản phẩm:**
1. Vào OQC → Tab Sản phẩm → Nhấn **Import Excel**
2. Chọn file `.xlsx` định dạng:
   - Cột A: Mã SP, Cột B: Tên SP, Cột C: Đặc tính, Cột D: Đơn vị

---

## 14. ĐỔI MẬT KHẨU

1. Nhấn vào **tên người dùng** ở góc phải màn hình
2. Chọn **Đổi mật khẩu**
3. Nhập: Mật khẩu cũ + Mật khẩu mới (tối thiểu 6 ký tự)
4. Nhấn **Đổi mật khẩu**

---

## 15. CÀI ĐẶT PWA (APP ĐIỆN THOẠI)

Cài app Quality MES như app native trên điện thoại, có icon ngoài màn hình, không hiện thanh địa chỉ trình duyệt.

### Android (Chrome)

1. Mở Chrome, vào link app (VD: `https://quality-mes-9.onrender.com`)
2. Đăng nhập → Bấm **3 chấm** góc phải trên
3. Chọn **Thêm vào màn hình chính**
4. Đặt tên → **Thêm**

### iOS / iPhone / iPad (Safari)

1. Mở Safari, vào link app
2. Bấm nút **Chia sẻ** (hình vuông mũi tên giữa thanh dưới)
3. Chọn **Thêm vào màn hình chính**
4. Đặt tên → **Thêm**

### Sau khi cài

- Mở app từ icon ngoài màn hình
- Giao diện toàn màn hình, không có thanh địa chỉ trình duyệt
- Dùng như app bình thường
- Tự động cập nhật khi có phiên bản mới

---

## 16. DEPLOY ONLINE 24/7 (RENDER)

Deploy app lên Render để truy cập online miễn phí 24/7.

### Bước 1: Push code lên GitHub

```powershell
cd C:\Users\BOD-Hung\Documents\Opencode
git push
```

### Bước 2: Tạo Web Service trên Render

1. Vào https://dashboard.render.com → Đăng nhập GitHub
2. **New +** → **Web Service** → Chọn repo `Hungton60/quality-mes`
3. Điền:

| Ô | Giá trị |
|---|---------|
| Root Directory | `quality-mes` |
| Build Command | `bash build.sh` |
| Start Command | `bash start.sh` |

4. Instance Type: **Free**
5. Nhấn **Create Web Service** → Đợi 5-7 phút build

Khi thấy `Your service is live 🎉` → Copy link chia sẻ cho team.

### Lưu ý

- Miễn phí 750 giờ/tháng (đủ dùng 24/7)
- Cold start 30-60 giây lần đầu truy cập
- App ngủ sau 15 phút không dùng → mở lại đợi vài giây
- Dữ liệu SQLite reset khi deploy code mới

---

## 17. TÍCH HỢP API

Quality MES cung cấp **REST API** để tích hợp với các hệ thống khác (ERP, MES, SCADA, BI...).

### 17.1. Truy cập tài liệu API

Mở trình duyệt: `http://địa-chỉ-máy:8000/api/docs`

Giao diện Swagger UI cho phép test trực tiếp mọi API.

### 17.2. Xác thực API

Tất cả API (trừ đăng nhập/đăng ký) cần gửi kèm JWT token trong header:

```
Authorization: Bearer <token>
```

**Lấy token:**
```
POST /api/auth/login
Body: {"username": "admin", "password": "Admin123"}
Response: {"access_token": "eyJ...", "token_type": "bearer", "user": {...}}
```

### 17.3. Ví dụ tích hợp

**Python:**
```python
import requests

BASE = "http://192.168.1.5:8000"

# Đăng nhập
r = requests.post(f"{BASE}/api/auth/login",
    json={"username": "admin", "password": "Admin123"})
token = r.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Tạo phiếu IQC
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

# Lấy thống kê chất lượng
stats = requests.get(f"{BASE}/api/spc/summary", headers=headers).json()
print(f"IQC: {stats['iqc']['total']} phiếu, Đạt: {stats['iqc']['pass']}")
```

### 17.4. Danh sách API endpoints

| Method | URL | Mô tả |
|--------|-----|-------|
| POST | `/api/auth/login` | Đăng nhập, lấy token |
| POST | `/api/auth/register` | Đăng ký tài khoản |
| GET | `/api/auth/me` | Thông tin người dùng hiện tại |
| GET | `/api/iqc/suppliers` | Danh sách nhà cung cấp |
| POST | `/api/iqc/suppliers` | Thêm nhà cung cấp |
| GET | `/api/iqc/materials` | Danh sách nguyên liệu |
| POST | `/api/iqc/materials` | Thêm nguyên liệu |
| GET | `/api/iqc/inspections` | Danh sách phiếu IQC |
| POST | `/api/iqc/inspections` | Tạo phiếu IQC |
| POST | `/api/iqc/inspections/{id}/results` | Thêm kết quả IQC |
| GET | `/api/oqc/products` | Danh sách sản phẩm |
| POST | `/api/oqc/products` | Thêm sản phẩm |
| GET | `/api/oqc/inspections` | Danh sách phiếu OQC |
| POST | `/api/oqc/inspections` | Tạo phiếu OQC |
| GET | `/api/ipqc/inspections` | Danh sách phiếu IPQC |
| POST | `/api/ipqc/inspections` | Tạo phiếu IPQC |
| GET | `/api/ncr/` | Danh sách NCR |
| POST | `/api/ncr/` | Tạo NCR |
| PUT | `/api/ncr/{id}/status` | Cập nhật trạng thái NCR |
| POST | `/api/ncr/{id}/capas` | Thêm CAPA cho NCR |
| GET | `/api/spc/summary` | Thống kê tổng quan |
| GET | `/api/overdue` | NCR/CAPA quá hạn |
| GET | `/api/equipment/` | Danh sách thiết bị |
| POST | `/api/equipment/` | Thêm thiết bị |
| PUT | `/api/equipment/{id}/calibrate` | Hiệu chuẩn thiết bị |
| GET | `/api/export/inspections` | Xuất Excel phiếu kiểm tra |
| POST | `/api/import/materials` | Import Excel nguyên liệu |
| POST | `/api/import/products` | Import Excel sản phẩm |
| GET | `/api/users/` | Danh sách người dùng (admin) |
| POST | `/api/users/` | Thêm người dùng (admin) |
| GET | `/api/users/lookup` | Tìm người dùng (dropdown) |
| GET | `/api/activity-logs` | Nhật ký hoạt động |
| POST | `/api/change-password` | Đổi mật khẩu |
| GET | `/api/aql-table` | Bảng tra AQL |
| GET | `/api/checklists/` | Danh sách checklist mẫu |
| POST | `/api/checklists/` | Tạo checklist mới |
| POST | `/api/checklists/import-excel` | Import checklist từ Excel/Word |

### 17.5. Tích hợp database trực tiếp

Có thể kết nối trực tiếp đến database SQLite để đọc dữ liệu:

**Power BI / Excel:**
1. Get Data → ODBC → SQLite
2. Chọn file `quality_mes.db`

**Python script:**
```python
import sqlite3
conn = sqlite3.connect("quality_mes.db")
df = pd.read_sql("SELECT * FROM iqc_inspections", conn)
```

---

## PHỤ LỤC: CÁCH KHÔI PHỤC DỮ LIỆU

### Reset toàn bộ dữ liệu

```powershell
cd quality-mes\backend
# Xóa database cũ
del quality_mes.db
# Tạo lại dữ liệu mẫu
python seed.py
python deploy.py
```

### Sao lưu dữ liệu

```powershell
# Copy file database
copy quality-mes\backend\quality_mes.db D:\Backup\quality_mes_backup.db
```

---

## HỖ TRỢ

- **API Docs:** `http://địa-chỉ-máy:8000/api/docs`
- **GitHub Issues:** Tạo issue trên repo GitHub
- **Liên hệ:** Bộ phận IT / Quản lý hệ thống

---

*Quality MES v1.0 - Tài liệu cập nhật 05/2026*
