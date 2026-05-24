from app.core.database import SessionLocal, init_db
from app.models.user import User
from app.models.iqc import Supplier, Material, IQCInspection, IQCResult
from app.models.oqc import Product, OQCInspection, OQCResult
from app.models.ipqc import IPQCInspection, IPQCResult
from app.models.ncr import NCR, CAPA
from app.auth.security import hash_password
from datetime import datetime


def seed():
    init_db()
    db = SessionLocal()

    # ---- Users ----
    if db.query(User).filter(User.username == "admin").first():
        print("Data already seeded, skipping.")
        db.close()
        return

    admin = User(username="admin", email="admin@may.com", hashed_password=hash_password("Admin123"), full_name="Quan ly", role="admin")
    qc = User(username="qc_manager", email="qc@may.com", hashed_password=hash_password("Qc123456"), full_name="Truong QC", role="qc_manager")
    insp1 = User(username="inspector1", email="insp1@may.com", hashed_password=hash_password("Insp123456"), full_name="Kiem tra vien A", role="inspector")
    insp2 = User(username="inspector2", email="insp2@may.com", hashed_password=hash_password("Insp123456"), full_name="Kiem tra vien B", role="inspector")
    oper = User(username="operator", email="oper@may.com", hashed_password=hash_password("Oper123456"), full_name="Cong nhan 1", role="operator")
    db.add_all([admin, qc, insp1, insp2, oper])
    db.commit()

    # ---- Suppliers ----
    s1 = Supplier(code="NCC001", name="Cong ty TNHH Thep Viet", contact_person="Nguyen Van A", phone="0901234567", email="thepviet@email.com")
    s2 = Supplier(code="NCC002", name="Cong ty CP Nhua Binh Minh", contact_person="Tran Thi B", phone="0912345678", email="nhuabm@email.com")
    s3 = Supplier(code="NCC003", name="Cong ty TNHH Kim Loai Dong A", contact_person="Le Van C", phone="0923456789", email="dongakl@email.com")
    db.add_all([s1, s2, s3])
    db.commit()

    # ---- Materials ----
    m1 = Material(code="VL001", name="Thep tam 2mm", specification="Day 2.0mm +/- 0.1mm, Rong 1200mm", unit="kg", supplier_id=s1.id)
    m2 = Material(code="VL002", name="Thep ong D21", specification="Duong kinh ngoai 21mm, day 1.5mm", unit="cay", supplier_id=s1.id)
    m3 = Material(code="VL003", name="Hat nhua PP", specification="PP nguyen sinh, chi so chay 12", unit="kg", supplier_id=s2.id)
    m4 = Material(code="VL004", name="Bu long M10", specification="M10x1.5, cap ben 8.8", unit="con", supplier_id=s3.id)
    db.add_all([m1, m2, m3, m4])
    db.commit()

    # ---- Products ----
    p1 = Product(code="SP001", name="Khung thep han", specification="1200x800mm, son tinh dien", unit="cai")
    p2 = Product(code="SP002", name="Ong nhua PVC D21", specification="D21, chiu ap luc 10 bar", unit="met")
    p3 = Product(code="SP003", name="Cum bu long dai oc M10", specification="M10x1.5, kem ma", unit="bo")
    db.add_all([p1, p2, p3])
    db.commit()

    now = datetime.now()

    # ---- IQC Inspections ----
    iqc1 = IQCInspection(inspection_no="IQC-2026-001", material_id=m1.id, supplier_id=s1.id, lot_no="LOT-THEP-001", quantity=5000, sample_size=50, inspection_date=now, inspector_id=insp1.id, status="pass")
    iqc2 = IQCInspection(inspection_no="IQC-2026-002", material_id=m3.id, supplier_id=s2.id, lot_no="LOT-NHUA-045", quantity=3000, sample_size=35, inspection_date=now, inspector_id=insp2.id, status="pass")
    iqc3 = IQCInspection(inspection_no="IQC-2026-003", material_id=m4.id, supplier_id=s3.id, lot_no="LOT-BL-102", quantity=10000, sample_size=80, inspection_date=now, inspector_id=insp1.id, status="fail")
    db.add_all([iqc1, iqc2, iqc3])
    db.commit()

    db.add_all([
        IQCResult(inspection_id=iqc1.id, item_name="Do day", specification="2.0mm +/- 0.1", measured_value=2.02, standard_min=1.9, standard_max=2.1, result="pass"),
        IQCResult(inspection_id=iqc1.id, item_name="Do rong", specification="1200mm +/- 2", measured_value=1199, standard_min=1198, standard_max=1202, result="pass"),
        IQCResult(inspection_id=iqc1.id, item_name="Do cung", specification="60-65 HRB", measured_value=62.5, standard_min=60, standard_max=65, result="pass"),
        IQCResult(inspection_id=iqc2.id, item_name="Chi so chay", specification="10-14", measured_value=12.1, standard_min=10, standard_max=14, result="pass"),
        IQCResult(inspection_id=iqc2.id, item_name="Do am", specification="<0.1%", measured_value=0.05, standard_max=0.1, result="pass"),
        IQCResult(inspection_id=iqc3.id, item_name="Duong kinh", specification="M10x1.5", measured_value=9.85, standard_min=9.9, standard_max=10.1, result="fail"),
        IQCResult(inspection_id=iqc3.id, item_name="Chieu dai", specification="50mm +/- 1", measured_value=48.2, standard_min=49, standard_max=51, result="fail"),
    ])
    db.commit()

    # ---- OQC Inspections ----
    oqc1 = OQCInspection(inspection_no="OQC-2026-001", product_id=p1.id, lot_no="LOT-KHUNG-011", quantity=200, sample_size=20, inspection_date=now, inspector_id=insp1.id, status="pass")
    oqc2 = OQCInspection(inspection_no="OQC-2026-002", product_id=p2.id, lot_no="LOT-ONG-056", quantity=1000, sample_size=32, inspection_date=now, inspector_id=insp2.id, status="pass")
    db.add_all([oqc1, oqc2])
    db.commit()

    db.add_all([
        OQCResult(inspection_id=oqc1.id, item_name="Kich thuoc", specification="1200x800 +/-2", measured_value=1200, standard_min=1198, standard_max=1202, result="pass"),
        OQCResult(inspection_id=oqc1.id, item_name="Do phang", specification="<1mm/m", measured_value=0.5, standard_max=1, result="pass"),
        OQCResult(inspection_id=oqc2.id, item_name="Duong kinh", specification="D21 +/- 0.2", measured_value=21.05, standard_min=20.8, standard_max=21.2, result="pass"),
        OQCResult(inspection_id=oqc2.id, item_name="Ap luc", specification=">=10 bar", measured_value=12.3, standard_min=10, result="pass"),
    ])
    db.commit()

    # ---- IPQC Inspections ----
    ipqc1 = IPQCInspection(inspection_no="IPQC-2026-001", process_name="Han khung", work_center="Tram han 1", machine="May han MIG-03", shift="Ca 1", inspection_date=now, inspector_id=insp1.id, sample_size=5, status="pass")
    ipqc2 = IPQCInspection(inspection_no="IPQC-2026-002", process_name="Son tinh dien", work_center="Tram son 2", machine="May phun son TL-01", shift="Ca 2", inspection_date=now, inspector_id=insp2.id, sample_size=5, status="fail")
    db.add_all([ipqc1, ipqc2])
    db.commit()

    db.add_all([
        IPQCResult(inspection_id=ipqc1.id, item_name="Moi han", specification="Ngon, deu", measured_value=8, standard_min=7, standard_max=10, result="pass"),
        IPQCResult(inspection_id=ipqc1.id, item_name="Khe ho", specification="<0.5mm", measured_value=0.3, standard_max=0.5, result="pass"),
        IPQCResult(inspection_id=ipqc2.id, item_name="Do day son", specification="60-80 micron", measured_value=45, standard_min=60, standard_max=80, result="fail"),
        IPQCResult(inspection_id=ipqc2.id, item_name="Do bong", specification=">=85 GU", measured_value=82, standard_min=85, result="fail"),
    ])
    db.commit()

    # ---- NCR + CAPA ----
    ncr1 = NCR(ncr_no="NCR-2026-001", title="Bu long M10 khong dat kich thuoc", description="Lo bu long LOT-BL-102 co nhieu con duong kinh va chieu dai nam ngoai dung sai.", severity="major", source_type="iqc", source_id=iqc3.id, reported_by=insp1.id, assigned_to=qc.id, status="investigating", due_date=datetime(2026, 6, 15))
    ncr2 = NCR(ncr_no="NCR-2026-002", title="Do day son khong dat tieu chuan", description="Ca 2 san xuat san pham son tinh dien co do day thap hon tieu chuan.", severity="minor", source_type="ipqc", source_id=ipqc2.id, reported_by=insp2.id, assigned_to=qc.id, status="open", due_date=datetime(2026, 6, 10))
    db.add_all([ncr1, ncr2])
    db.commit()

    db.add_all([
        CAPA(capa_no="CAPA-2026-001", ncr_id=ncr1.id, type="corrective", title="Tra lai lo hang bu long khong dat", description="Yeu cau NCC thu hoi va gui lo hang thay the.", root_cause="Nha cung cap khong kiem tra chat luong truoc khi giao.", action_plan="1. Gui thong bao cho NCC. 2. Yeu cau gui hang thay the trong 7 ngay. 3. Tang cuong kiem tra IQC.", assigned_to=insp1.id, status="in_progress", due_date=datetime(2026, 6, 20)),
        CAPA(capa_no="CAPA-2026-002", ncr_id=ncr1.id, type="preventive", title="Tang tan suat kiem tra IQC bu long", description="Tang mau IQC tu G-II len G-III cho nguyen lieu bu long.", assigned_to=qc.id, status="open", due_date=datetime(2026, 7, 1)),
        CAPA(capa_no="CAPA-2026-003", ncr_id=ncr2.id, type="corrective", title="Hieu chinh may phun son", description="Kiem tra va hieu chinh thong so may phun son TL-01.", root_cause="Ap luc phun thap hon cai dat.", action_plan="1. Kiem tra he thong khi nen. 2. Hieu chinh ap luc. 3. Test lai do day.", assigned_to=oper.id, status="open", due_date=datetime(2026, 6, 5)),
    ])
    db.commit()

    db.close()
    print("Seed data created successfully!")


if __name__ == "__main__":
    seed()
