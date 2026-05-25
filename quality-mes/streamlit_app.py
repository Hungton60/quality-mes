import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta

st.set_page_config(page_title="Quality MES", page_icon="📊", layout="wide")

from app.core.database import SessionLocal, init_db
from app.models.user import User
from app.models.iqc import Supplier, Material, IQCInspection, IQCResult
from app.models.oqc import Product, OQCInspection, OQCResult
from app.models.ipqc import IPQCInspection, IPQCResult
from app.models.ncr import NCR, CAPA
from app.models.equipment import Equipment, ActivityLog
from app.models.checklist import ChecklistTemplate
from app.auth.security import hash_password, verify_password

init_db()

def auto_seed():
    db = SessionLocal()
    if db.query(User).count() == 0:
        db.add_all([
            User(username="admin", email="admin@may.com", hashed_password=hash_password("Admin123"), full_name="Quan ly", role="admin"),
            User(username="qc_manager", email="qc@may.com", hashed_password=hash_password("Qc123456"), full_name="Truong QC", role="qc_manager"),
            User(username="inspector1", email="insp1@may.com", hashed_password=hash_password("Insp123456"), full_name="Kiem tra vien A", role="inspector"),
            User(username="inspector2", email="insp2@may.com", hashed_password=hash_password("Insp123456"), full_name="Kiem tra vien B", role="inspector"),
            User(username="operator", email="oper@may.com", hashed_password=hash_password("Oper123456"), full_name="Cong nhan 1", role="operator"),
        ])
        db.commit()
    db.close()

auto_seed()

ROLES = {"admin": "Quan ly", "qc_manager": "Truong QC", "inspector": "Kiem tra vien", "operator": "Cong nhan"}
STATUS_LABELS = {"pending": "Cho kiem", "pass": "Dat", "fail": "Khong dat"}
NCR_STATUS = {"open": "Mo", "investigating": "Dang dieu tra", "resolved": "Da xu ly", "closed": "Dong"}
CAPA_STATUS = {"open": "Mo", "in_progress": "Dang thuc hien", "completed": "Hoan thanh", "verified": "Da xac nhan"}
SEVERITY = {"critical": "Nghiem trong", "major": "Lon", "minor": "Nho"}


def get_db():
    return SessionLocal()


def login_page():
    st.title("Quality MES")
    st.subheader("He thong quan ly chat luong nha may")
    tab1, tab2 = st.tabs(["Dang nhap", "Dang ky"])
    with tab1:
        username = st.text_input("Ten dang nhap", key="login_user")
        password = st.text_input("Mat khau", type="password", key="login_pass")
        if st.button("Dang nhap", type="primary", use_container_width=True):
            db = get_db()
            user = db.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.hashed_password) and user.is_active:
                st.session_state.user_id = user.id
                st.session_state.username = user.username
                st.session_state.full_name = user.full_name
                st.session_state.role = user.role
                db.close()
                st.rerun()
            else:
                st.error("Sai ten dang nhap hoac mat khau")
                db.close()
    with tab2:
        with st.form("register_form"):
            full_name = st.text_input("Ho ten")
            email = st.text_input("Email")
            reg_user = st.text_input("Ten dang nhap")
            reg_pass = st.text_input("Mat khau", type="password")
            if st.form_submit_button("Dang ky", use_container_width=True):
                db = get_db()
                exist = db.query(User).filter((User.username == reg_user) | (User.email == email)).first()
                if exist:
                    st.error("Ten dang nhap hoac email da ton tai")
                else:
                    u = User(username=reg_user, email=email, hashed_password=hash_password(reg_pass), full_name=full_name, role="inspector")
                    db.add(u); db.commit()
                    st.success("Dang ky thanh cong! Hay dang nhap.")
                db.close()


def log_activity(db, action, module, description):
    try:
        log = ActivityLog(user_id=st.session_state.get("user_id", 1), username=st.session_state.get("username", "system"), action=action, module=module, description=description)
        db.add(log); db.commit()
    except: pass


def _opt(d, default="-- Chon --"):
    return [default] + list(d.keys()) if d else [default]


def dashboard_page():
    st.title("Bang dieu khien")
    db = get_db()
    iqc_total = db.query(IQCInspection).count()
    iqc_pass = db.query(IQCInspection).filter(IQCInspection.status == "pass").count()
    iqc_fail = db.query(IQCInspection).filter(IQCInspection.status == "fail").count()
    oqc_total = db.query(OQCInspection).count()
    oqc_pass = db.query(OQCInspection).filter(OQCInspection.status == "pass").count()
    oqc_fail = db.query(OQCInspection).filter(OQCInspection.status == "fail").count()
    ipqc_total = db.query(IPQCInspection).count()
    ipqc_pass = db.query(IPQCInspection).filter(IPQCInspection.status == "pass").count()
    ipqc_fail = db.query(IPQCInspection).filter(IPQCInspection.status == "fail").count()
    total = iqc_total + oqc_total + ipqc_total
    total_pass = iqc_pass + oqc_pass + ipqc_pass
    total_fail = iqc_fail + oqc_fail + ipqc_fail
    pass_rate = (total_pass / total * 100) if total > 0 else 0
    open_ncr = db.query(NCR).filter(NCR.status.in_(["open", "investigating"])).count()
    overdue_ncr = db.query(NCR).filter(NCR.status.in_(["open", "investigating"]), NCR.due_date.isnot(None), NCR.due_date < datetime.now()).count()
    overdue_capa = db.query(CAPA).filter(CAPA.status.in_(["open", "in_progress"]), CAPA.due_date.isnot(None), CAPA.due_date < datetime.now()).count()
    db.close()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tong phieu kiem tra", total)
    col2.metric("Dat", total_pass)
    col3.metric("Khong dat", total_fail, delta_color="inverse")
    col4.metric("Ty le dat", f"{pass_rate:.1f}%")

    col1, col2, col3 = st.columns(3)
    col1.metric("NCR dang mo", open_ncr)
    col2.metric("NCR qua han", overdue_ncr)
    col3.metric("CAPA qua han", overdue_capa)

    if overdue_ncr > 0 or overdue_capa > 0:
        st.warning(f"⚠️ Canh bao: {overdue_ncr} NCR va {overdue_capa} CAPA qua han!")


def supplier_tab(db):
    st.subheader("Nha cung cap")
    with st.form("supplier_form"):
        cols = st.columns([1, 2, 1, 1, 2, 2])
        code = cols[0].text_input("Ma NCC")
        name = cols[1].text_input("Ten NCC")
        contact = cols[2].text_input("Nguoi LH")
        phone = cols[3].text_input("SDT")
        email = cols[4].text_input("Email")
        addr = cols[5].text_input("Dia chi")
        if st.form_submit_button("Them NCC", type="primary"):
            if code and name:
                exist = db.query(Supplier).filter(Supplier.code == code).first()
                if exist: st.error("Ma NCC da ton tai")
                else:
                    db.add(Supplier(code=code, name=name, contact_person=contact, phone=phone, email=email, address=addr))
                    db.commit(); log_activity(db, "create", "iqc", f"Them NCC {code}")
                    st.success("Them NCC thanh cong!"); st.rerun()
    suppliers = db.query(Supplier).order_by(Supplier.name).all()
    if suppliers:
        df = pd.DataFrame([{"Ma": s.code, "Ten": s.name, "Nguoi LH": s.contact_person or "", "SDT": s.phone or "", "Email": s.email or ""} for s in suppliers])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Chua co nha cung cap nao. Hay them NCC o tren.")


def material_tab(db):
    st.subheader("Nguyen vat lieu")
    suppliers = db.query(Supplier).order_by(Supplier.name).all()
    sup_map = {s.name: s.id for s in suppliers}

    if not suppliers:
        st.warning("Vui long them Nha cung cap truoc khi them Nguyen lieu.")
        return

    with st.form("material_form"):
        cols = st.columns([1, 2, 1, 1, 2])
        code = cols[0].text_input("Ma NL")
        name = cols[1].text_input("Ten NL")
        spec = cols[2].text_input("Dac tinh")
        unit = cols[3].text_input("Don vi", value="pcs")
        sup_name = cols[4].selectbox("NCC", options=list(sup_map.keys()), key="mat_ncc")
        if st.form_submit_button("Them NL", type="primary"):
            if code and name and sup_name in sup_map:
                exist = db.query(Material).filter(Material.code == code).first()
                if exist: st.error("Ma NL da ton tai")
                else:
                    db.add(Material(code=code, name=name, specification=spec, unit=unit, supplier_id=sup_map[sup_name]))
                    db.commit(); log_activity(db, "create", "iqc", f"Them NL {code}")
                    st.success("Them NL thanh cong!"); st.rerun()
    materials = db.query(Material).order_by(Material.name).all()
    if materials:
        df = pd.DataFrame([{"Ma": m.code, "Ten": m.name, "Dac tinh": m.specification or "", "DV": m.unit, "NCC": m.supplier.name if m.supplier else ""} for m in materials])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Chua co nguyen lieu nao.")


def iqc_inspection_tab(db):
    st.subheader("Phieu kiem tra IQC")

    suppliers = db.query(Supplier).order_by(Supplier.name).all()
    materials = db.query(Material).order_by(Material.name).all()
    if not suppliers or not materials:
        st.warning("Vui long them Nha cung cap va Nguyen lieu truoc.")
        return

    users = db.query(User).filter(User.is_active == True).order_by(User.full_name).all()
    user_map = {u.full_name: u.id for u in users}
    mat_map = {m.name: m.id for m in materials}
    sup_map = {s.name: s.id for s in suppliers}

    with st.expander("Tao phieu kiem tra moi", expanded=False):
        with st.form("iqc_insp_form"):
            cols = st.columns([2, 2, 2, 1, 1, 1])
            insp_no = cols[0].text_input("So phieu")
            mat_name = cols[1].selectbox("Nguyen lieu", options=list(mat_map.keys()), key="iqc_mat")
            sup_name = cols[2].selectbox("Nha cung cap", options=list(sup_map.keys()), key="iqc_sup")
            lot = cols[3].text_input("So lo")
            qty = cols[4].number_input("So luong", 1, 99999, 1000)
            sample = cols[5].number_input("Co mau", 1, 100, 20)
            cols2 = st.columns([2, 2, 2])
            insp_date = cols2[0].date_input("Ngay kiem", value=date.today())
            insp_name = cols2[1].selectbox("Nguoi kiem", options=list(user_map.keys()), key="iqc_user")
            notes = cols2[2].text_input("Ghi chu")
            checklists = db.query(ChecklistTemplate).filter(ChecklistTemplate.module == "iqc").all()
            cl_map = {f"{c.name} ({len(c.items or [])} muc)": c for c in checklists}
            cl_name = st.selectbox("Checklist mau (tu dong dien muc)", options=["-- Khong dung --"] + list(cl_map.keys()), key="iqc_cl")
            if st.form_submit_button("Tao phieu", type="primary"):
                if insp_no and mat_name in mat_map and sup_name in sup_map and lot:
                    exist = db.query(IQCInspection).filter(IQCInspection.inspection_no == insp_no).first()
                    if exist: st.error("So phieu da ton tai")
                    else:
                        insp = IQCInspection(inspection_no=insp_no, material_id=mat_map[mat_name], supplier_id=sup_map[sup_name], lot_no=lot, quantity=qty, sample_size=sample, inspection_date=datetime.combine(insp_date, datetime.min.time()), inspector_id=user_map[insp_name], notes=notes)
                        db.add(insp); db.commit()
                        ref = db.refresh
                        if cl_name != "-- Khong dung --" and cl_name in cl_map:
                            for item in cl_map[cl_name].items or []:
                                db.add(IQCResult(inspection_id=insp.id, item_name=item.get("item_name",""), specification=item.get("specification",""), measured_value=0, standard_min=item.get("standard_min"), standard_max=item.get("standard_max"), result="pass"))
                            db.commit()
                        log_activity(db, "create", "iqc", f"Tao phieu IQC {insp_no}")
                        st.success("Tao phieu thanh cong!"); st.rerun()
                else:
                    st.error("Vui long nhap day du thong tin.")

    inspections = db.query(IQCInspection).order_by(IQCInspection.created_at.desc()).limit(30).all()
    if not inspections:
        st.info("Chua co phieu IQC nao.")
        return

    for insp in inspections:
        with st.expander(f"{insp.inspection_no} - {insp.material.name if insp.material else 'N/A'} ({STATUS_LABELS.get(insp.status, insp.status)})"):
            st.write(f"**NCC:** {insp.supplier.name if insp.supplier else 'N/A'} | **Lo:** {insp.lot_no} | **SL/Sample:** {insp.quantity}/{insp.sample_size}")
            results = db.query(IQCResult).filter(IQCResult.inspection_id == insp.id).all()
            if results:
                rdf = pd.DataFrame([{"Muc kiem": r.item_name, "Tieu chuan": r.specification or "", "Gia tri do": r.measured_value, "Min": r.standard_min, "Max": r.standard_max, "KQ": "Dat" if r.result == "pass" else "Khong dat"} for r in results])
                st.dataframe(rdf, use_container_width=True, hide_index=True)
            if insp.status == "pending":
                c1, c2, c3 = st.columns(3)
                if c1.button("Dat", key=f"iqc_pass_{insp.id}"): insp.status = "pass"; db.commit(); st.rerun()
                if c2.button("Khong dat", key=f"iqc_fail_{insp.id}"): insp.status = "fail"; db.commit(); st.rerun()
            with st.form(f"iqc_res_{insp.id}"):
                c1, c2, c3, c4 = st.columns(4)
                item = c1.text_input("Muc kiem", key=f"iqc_item_{insp.id}")
                measured = c2.number_input("Gia tri do", value=0.0, format="%.3f", key=f"iqc_mv_{insp.id}")
                min_v = c3.number_input("Min", value=0.0, format="%.3f", key=f"iqc_min_{insp.id}")
                max_v = c4.number_input("Max", value=0.0, format="%.3f", key=f"iqc_max_{insp.id}")
                if st.form_submit_button("Them ket qua"):
                    if item:
                        r = "pass" if min_v <= measured <= max_v else "fail"
                        db.add(IQCResult(inspection_id=insp.id, item_name=item, measured_value=measured, standard_min=min_v, standard_max=max_v, result=r))
                        db.commit(); st.rerun()


def iqc_page():
    st.title("Kiem tra dau vao (IQC)")
    db = get_db()
    tab1, tab2, tab3 = st.tabs(["Phieu kiem tra", "Nha cung cap", "Nguyen vat lieu"])
    with tab1: iqc_inspection_tab(db)
    with tab2: supplier_tab(db)
    with tab3: material_tab(db)
    db.close()


def oqc_page():
    st.title("Kiem tra thanh pham (OQC)")
    db = get_db()
    tab1, tab2 = st.tabs(["Phieu kiem tra", "San pham"])

    with tab2:
        st.subheader("San pham")
        with st.form("product_form"):
            c1, c2, c3, c4 = st.columns(4)
            code = c1.text_input("Ma SP")
            name = c2.text_input("Ten SP")
            spec = c3.text_input("Dac tinh")
            unit = c4.text_input("Don vi", value="pcs")
            if st.form_submit_button("Them san pham", type="primary"):
                if code and name:
                    exist = db.query(Product).filter(Product.code == code).first()
                    if exist: st.error("Ma SP da ton tai")
                    else:
                        db.add(Product(code=code, name=name, specification=spec, unit=unit))
                        db.commit(); log_activity(db, "create", "oqc", f"Them SP {code}")
                        st.success("Them SP thanh cong!"); st.rerun()
        products = db.query(Product).order_by(Product.name).all()
        if products:
            df = pd.DataFrame([{"Ma": p.code, "Ten": p.name, "Dac tinh": p.specification or "", "DV": p.unit} for p in products])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Chua co san pham nao.")

    with tab1:
        st.subheader("Phieu kiem tra OQC")
        products = db.query(Product).order_by(Product.name).all()
        if not products:
            st.warning("Vui long them San pham truoc.")
            db.close()
            return

        users = db.query(User).filter(User.is_active == True).order_by(User.full_name).all()
        user_map = {u.full_name: u.id for u in users}
        prod_map = {p.name: p.id for p in products}

        with st.expander("Tao phieu kiem tra moi", expanded=False):
            with st.form("oqc_insp_form"):
                c1, c2, c3, c4, c5, c6 = st.columns(6)
                insp_no = c1.text_input("So phieu", key="oqc_no")
                prod_name = c2.selectbox("San pham", options=list(prod_map.keys()), key="oqc_prod")
                lot = c3.text_input("So lo", key="oqc_lot")
                qty = c4.number_input("So luong", 1, 99999, 500, key="oqc_qty")
                sample = c5.number_input("Co mau", 1, 100, 20, key="oqc_sample")
                insp_date = c6.date_input("Ngay kiem", value=date.today(), key="oqc_date")
                c7, c8 = st.columns(2)
                insp_name = c7.selectbox("Nguoi kiem", options=list(user_map.keys()), key="oqc_insp")
                notes = c8.text_input("Ghi chu", key="oqc_notes")
                if st.form_submit_button("Tao phieu", type="primary"):
                    if insp_no and prod_name in prod_map and lot:
                        exist = db.query(OQCInspection).filter(OQCInspection.inspection_no == insp_no).first()
                        if exist: st.error("So phieu da ton tai")
                        else:
                            insp = OQCInspection(inspection_no=insp_no, product_id=prod_map[prod_name], lot_no=lot, quantity=qty, sample_size=sample, inspection_date=datetime.combine(insp_date, datetime.min.time()), inspector_id=user_map[insp_name], notes=notes)
                            db.add(insp); db.commit()
                            log_activity(db, "create", "oqc", f"Tao phieu OQC {insp_no}")
                            st.success("Tao phieu thanh cong!"); st.rerun()

        inspections = db.query(OQCInspection).order_by(OQCInspection.created_at.desc()).limit(30).all()
        if not inspections:
            st.info("Chua co phieu OQC nao.")
            db.close()
            return

        for insp in inspections:
            with st.expander(f"{insp.inspection_no} - {insp.product.name if insp.product else 'N/A'} ({STATUS_LABELS.get(insp.status, insp.status)})"):
                st.write(f"**Lo:** {insp.lot_no} | **SL/Sample:** {insp.quantity}/{insp.sample_size}")
                results = db.query(OQCResult).filter(OQCResult.inspection_id == insp.id).all()
                if results:
                    rdf = pd.DataFrame([{"Muc kiem": r.item_name, "Do": r.measured_value, "Min": r.standard_min, "Max": r.standard_max, "KQ": "Dat" if r.result == "pass" else "Khong dat"} for r in results])
                    st.dataframe(rdf, use_container_width=True, hide_index=True)
                if insp.status == "pending":
                    c1, c2 = st.columns(2)
                    if c1.button("Dat", key=f"oqc_pass_{insp.id}"): insp.status = "pass"; db.commit(); st.rerun()
                    if c2.button("Khong dat", key=f"oqc_fail_{insp.id}"): insp.status = "fail"; db.commit(); st.rerun()
                with st.form(f"oqc_res_{insp.id}"):
                    c1, c2, c3, c4 = st.columns(4)
                    item = c1.text_input("Muc kiem", key=f"oqc_item_{insp.id}")
                    measured = c2.number_input("Gia tri do", value=0.0, format="%.3f", key=f"oqc_mv_{insp.id}")
                    min_v = c3.number_input("Min", value=0.0, format="%.3f", key=f"oqc_min_{insp.id}")
                    max_v = c4.number_input("Max", value=0.0, format="%.3f", key=f"oqc_max_{insp.id}")
                    if st.form_submit_button("Them ket qua"):
                        if item:
                            r = "pass" if (min_v <= measured <= max_v) else "fail"
                            db.add(OQCResult(inspection_id=insp.id, item_name=item, measured_value=measured, standard_min=min_v, standard_max=max_v, result=r))
                            db.commit(); st.rerun()
    db.close()


def ipqc_page():
    st.title("Kiem tra qua trinh (IPQC)")
    db = get_db()
    users = db.query(User).filter(User.is_active == True).order_by(User.full_name).all()
    user_map = {u.full_name: u.id for u in users}

    with st.expander("Tao phieu kiem tra moi", expanded=False):
        with st.form("ipqc_insp_form"):
            c1, c2, c3 = st.columns(3)
            insp_no = c1.text_input("So phieu")
            process = c2.text_input("Cong doan")
            wc = c3.text_input("Tram lam viec")
            c4, c5, c6 = st.columns(3)
            machine = c4.text_input("May")
            shift = c5.selectbox("Ca", ["Ca 1", "Ca 2", "Ca 3"])
            sample = c6.number_input("Co mau", 1, 25, 5)
            c7, c8 = st.columns(2)
            insp_date = c7.date_input("Ngay kiem", value=date.today())
            insp_name = c8.selectbox("Nguoi kiem", options=list(user_map.keys()), key="ipqc_user")
            if st.form_submit_button("Tao phieu", type="primary"):
                if insp_no and process and wc and insp_name in user_map:
                    exist = db.query(IPQCInspection).filter(IPQCInspection.inspection_no == insp_no).first()
                    if exist: st.error("So phieu da ton tai")
                    else:
                        insp = IPQCInspection(inspection_no=insp_no, process_name=process, work_center=wc, machine=machine, shift=shift, sample_size=sample, inspection_date=datetime.combine(insp_date, datetime.min.time()), inspector_id=user_map[insp_name])
                        db.add(insp); db.commit()
                        log_activity(db, "create", "ipqc", f"Tao phieu IPQC {insp_no}")
                        st.success("Tao phieu thanh cong!"); st.rerun()

    inspections = db.query(IPQCInspection).order_by(IPQCInspection.created_at.desc()).limit(30).all()
    if not inspections:
        st.info("Chua co phieu IPQC nao.")
        db.close()
        return

    for insp in inspections:
        with st.expander(f"{insp.inspection_no} - {insp.process_name} ({STATUS_LABELS.get(insp.status, insp.status)})"):
            st.write(f"**Tram:** {insp.work_center} | **May:** {insp.machine or 'N/A'} | **Ca:** {insp.shift} | **Sample:** {insp.sample_size}")
            results = db.query(IPQCResult).filter(IPQCResult.inspection_id == insp.id).all()
            if results:
                rdf = pd.DataFrame([{"Muc kiem": r.item_name, "Do": r.measured_value, "Min": r.standard_min, "Max": r.standard_max, "KQ": "Dat" if r.result == "pass" else "Khong dat"} for r in results])
                st.dataframe(rdf, use_container_width=True, hide_index=True)
            if insp.status == "pending":
                c1, c2 = st.columns(2)
                if c1.button("Dat", key=f"ipqc_pass_{insp.id}"): insp.status = "pass"; db.commit(); st.rerun()
                if c2.button("Khong dat", key=f"ipqc_fail_{insp.id}"): insp.status = "fail"; db.commit(); st.rerun()
            with st.form(f"ipqc_res_{insp.id}"):
                c1, c2, c3, c4 = st.columns(4)
                item = c1.text_input("Muc kiem", key=f"ipqc_item_{insp.id}")
                measured = c2.number_input("Gia tri do", value=0.0, format="%.3f", key=f"ipqc_mv_{insp.id}")
                min_v = c3.number_input("Min", value=0.0, format="%.3f", key=f"ipqc_min_{insp.id}")
                max_v = c4.number_input("Max", value=0.0, format="%.3f", key=f"ipqc_max_{insp.id}")
                if st.form_submit_button("Them ket qua"):
                    if item:
                        r = "pass" if (min_v <= measured <= max_v) else "fail"
                        db.add(IPQCResult(inspection_id=insp.id, item_name=item, measured_value=measured, standard_min=min_v, standard_max=max_v, result=r))
                        db.commit(); st.rerun()
    db.close()


def ncr_page():
    st.title("NCR + CAPA")
    db = get_db()
    users = db.query(User).filter(User.is_active == True).order_by(User.full_name).all()
    user_map = {u.full_name: u.id for u in users}

    tab1, tab2 = st.tabs(["NCR", "CAPA"])

    with tab1:
        with st.expander("Tao NCR moi", expanded=False):
            with st.form("ncr_form"):
                c1, c2 = st.columns(2)
                ncr_no = c1.text_input("So NCR")
                title = c2.text_input("Tieu de")
                desc = st.text_area("Mo ta")
                c3, c4, c5 = st.columns(3)
                severity = c3.selectbox("Muc do", options=list(SEVERITY.keys()), format_func=lambda x: SEVERITY[x])
                source_type = c4.selectbox("Nguon", ["iqc", "oqc", "ipqc", "other"])
                reporter = c5.selectbox("Nguoi bao cao", options=list(user_map.keys()))
                c6, c7 = st.columns(2)
                assignee = c6.selectbox("Nguoi xu ly", options=["-- Chua phan cong --"] + list(user_map.keys()))
                due = c7.date_input("Han xu ly")
                if st.form_submit_button("Tao NCR", type="primary"):
                    if ncr_no and title:
                        exist = db.query(NCR).filter(NCR.ncr_no == ncr_no).first()
                        if exist: st.error("So NCR da ton tai")
                        else:
                            n = NCR(ncr_no=ncr_no, title=title, description=desc, severity=severity, source_type=source_type, reported_by=user_map[reporter], assigned_to=user_map.get(assignee), due_date=datetime.combine(due, datetime.min.time()) if due else None)
                            db.add(n); db.commit()
                            log_activity(db, "create", "ncr", f"Tao NCR {ncr_no}")
                            st.success("Tao NCR thanh cong!"); st.rerun()

        ncrs = db.query(NCR).order_by(NCR.created_at.desc()).limit(30).all()
        if not ncrs:
            st.info("Chua co NCR nao.")
        else:
            for n in ncrs:
                with st.expander(f"{n.ncr_no} - {n.title} ({NCR_STATUS.get(n.status, n.status)})"):
                    st.write(f"**Muc do:** {SEVERITY.get(n.severity, n.severity)} | **Nguon:** {n.source_type or 'Khac'}")
                    st.write(f"**Mo ta:** {n.description}")
                    if n.resolution: st.write(f"**Giai phap:** {n.resolution}")
                    c1, c2, c3, c4 = st.columns(4)
                    if n.status == "open" and c1.button("Dieu tra", key=f"ncr_inv_{n.id}"): n.status = "investigating"; db.commit(); st.rerun()
                    if n.status == "investigating" and c2.button("Da xu ly", key=f"ncr_res_{n.id}"): n.status = "resolved"; db.commit(); st.rerun()
                    if n.status == "resolved" and c3.button("Dong", key=f"ncr_cls_{n.id}"): n.status = "closed"; db.commit(); st.rerun()

                    capas = db.query(CAPA).filter(CAPA.ncr_id == n.id).all()
                    if capas:
                        st.write("**CAPA:**")
                        for c in capas:
                            st.caption(f"  {c.capa_no} - {c.title} [{CAPA_STATUS.get(c.status, c.status)}]")

                    with st.form(f"capa_form_{n.id}"):
                        st.write("**Them CAPA moi:**")
                        c1, c2 = st.columns(2)
                        capa_no = c1.text_input("So CAPA", key=f"cno_{n.id}")
                        capa_title = c2.text_input("Tieu de CAPA", key=f"ctitle_{n.id}")
                        capa_desc = st.text_area("Mo ta CAPA", key=f"cdesc_{n.id}")
                        c3, c4, c5 = st.columns(3)
                        capa_type = c3.selectbox("Loai", ["corrective", "preventive"], format_func=lambda x: "Khac phuc" if x == "corrective" else "Phong ngua", key=f"ctype_{n.id}")
                        capa_assignee = c4.selectbox("Nguoi phu trach", options=["-- Chon --"] + list(user_map.keys()), key=f"cassign_{n.id}")
                        capa_due = c5.date_input("Han hoan thanh", key=f"cdue_{n.id}")
                        root_cause = st.text_input("Nguyen nhan goc", key=f"croot_{n.id}")
                        action = st.text_area("Ke hoach hanh dong", key=f"cact_{n.id}")
                        if st.form_submit_button("Them CAPA"):
                            if capa_no and capa_title:
                                ca = CAPA(capa_no=capa_no, ncr_id=n.id, type=capa_type, title=capa_title, description=capa_desc, root_cause=root_cause, action_plan=action, assigned_to=user_map.get(capa_assignee), due_date=datetime.combine(capa_due, datetime.min.time()) if capa_due else None)
                                db.add(ca); db.commit()
                                log_activity(db, "create", "capa", f"Tao CAPA {capa_no}")
                                st.success("Them CAPA thanh cong!"); st.rerun()

    with tab2:
        all_capas = db.query(CAPA).order_by(CAPA.created_at.desc()).limit(50).all()
        if all_capas:
            data = [{"So CAPA": c.capa_no, "Tieu de": c.title, "Loai": "Khac phuc" if c.type == "corrective" else "Phong ngua", "Status": CAPA_STATUS.get(c.status, c.status), "Han": str(c.due_date)[:10] if c.due_date else ""} for c in all_capas]
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
        else:
            st.info("Chua co CAPA nao.")

    db.close()


def spc_page():
    st.title("Bao cao thong ke (SPC)")
    db = get_db()
    tab1, tab2 = st.tabs(["Tong quan", "Bieu do"])

    with tab1:
        iqc_total = db.query(IQCInspection).count()
        oqc_total = db.query(OQCInspection).count()
        ipqc_total = db.query(IPQCInspection).count()
        ncr_open = db.query(NCR).filter(NCR.status.in_(["open", "investigating"])).count()
        ncr_closed = db.query(NCR).filter(NCR.status == "closed").count()

        c1, c2, c3, c4, c5, c6 = st.columns(6)
        c1.metric("IQC", iqc_total)
        c2.metric("IPQC", ipqc_total)
        c3.metric("OQC", oqc_total)
        c4.metric("NCR mo", ncr_open)
        c5.metric("NCR dong", ncr_closed)
        c6.metric("Tong phieu", iqc_total + oqc_total + ipqc_total)

    with tab2:
        module = st.selectbox("Chon module", ["iqc", "oqc", "ipqc"])
        model_map = {"iqc": IQCResult, "oqc": OQCResult, "ipqc": IPQCResult}
        results = db.query(model_map[module]).order_by(model_map[module].created_at.desc()).limit(200).all()
        if results:
            df = pd.DataFrame([{"Muc kiem": r.item_name, "Gia tri": r.measured_value, "Min": r.standard_min, "Max": r.standard_max} for r in results])
            fig = px.line(df, y="Gia tri", title=f"Xu huong do luong - {module.upper()}")
            st.plotly_chart(fig, use_container_width=True)

            fail_df = df[df["Gia tri"].apply(lambda _: True)]
            fail_items = [r for r in results if r.result == "fail"]
            if fail_items:
                fail_counts = pd.DataFrame([{"Muc kiem": r.item_name} for r in fail_items]).groupby("Muc kiem").size().reset_index(name="So loi")
                fig2 = px.bar(fail_counts, x="Muc kiem", y="So loi", title=f"Pareto loi - {module.upper()}", color="So loi")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Chua co du lieu do luong.")

    db.close()


def equipment_page():
    st.title("Thiet bi do & Hieu chuan")
    db = get_db()

    with st.expander("Them thiet bi", expanded=False):
        with st.form("equip_form"):
            c1, c2, c3 = st.columns(3)
            code = c1.text_input("Ma TB")
            name = c2.text_input("Ten TB")
            etype = c3.selectbox("Loai", ["measurement", "testing", "gauge", "other"])
            c4, c5, c6 = st.columns(3)
            serial = c4.text_input("So serie")
            location = c5.text_input("Vi tri")
            interval = c6.number_input("Chu ky hieu chuan (ngay)", 1, 3650, 365)
            c7, c8 = st.columns(2)
            last_cal = c7.date_input("Ngay hieu chuan cuoi", value=None)
            notes = c8.text_input("Ghi chu")
            if st.form_submit_button("Them TB", type="primary"):
                if code and name:
                    exist = db.query(Equipment).filter(Equipment.code == code).first()
                    if exist: st.error("Ma TB da ton tai")
                    else:
                        eq = Equipment(code=code, name=name, type=etype, serial_no=serial, location=location, calibration_interval_days=interval, last_calibration_date=last_cal, notes=notes)
                        if last_cal: eq.next_calibration_date = last_cal + timedelta(days=interval)
                        db.add(eq); db.commit()
                        log_activity(db, "create", "equipment", f"Them TB {code}")
                        st.success("Them TB thanh cong!"); st.rerun()

    today = date.today()
    equipments = db.query(Equipment).order_by(Equipment.name).all()
    if equipments:
        for eq in equipments:
            overdue = eq.next_calibration_date and eq.next_calibration_date < today
            days_left = (eq.next_calibration_date - today).days if eq.next_calibration_date else None
            icon = "🔴" if overdue else ("🟠" if days_left and days_left <= 30 else "🟢")
            with st.expander(f"{icon} {eq.code} - {eq.name}"):
                c1, c2, c3 = st.columns(3)
                c1.write(f"**Loai:** {eq.type}")
                c2.write(f"**Vi tri:** {eq.location or 'N/A'}")
                c3.write(f"**Chu ky:** {eq.calibration_interval_days} ngay")
                c4, c5 = st.columns(2)
                c4.write(f"**HC cuoi:** {eq.last_calibration_date}")
                c5.write(f"**Han HC:** {eq.next_calibration_date}")
                if overdue: st.error("⚠️ DA QUA HAN HIEU CHUAN!")
                elif days_left and days_left <= 30: st.warning(f"⚠️ Sap den han (con {days_left} ngay)")
                with st.form(f"cal_{eq.id}"):
                    cal_date = st.date_input("Ngay hieu chuan", value=today, key=f"caldt_{eq.id}")
                    if st.form_submit_button("Xac nhan hieu chuan"):
                        eq.last_calibration_date = cal_date
                        eq.next_calibration_date = cal_date + timedelta(days=eq.calibration_interval_days)
                        eq.status = "active"
                        db.commit()
                        log_activity(db, "calibrate", "equipment", f"Hieu chuan TB {eq.code}")
                        st.success("Hieu chuan thanh cong!"); st.rerun()
    else:
        st.info("Chua co thiet bi nao.")
    db.close()


def users_page():
    if st.session_state.role != "admin":
        st.error("Chi admin moi co quyen truy cap")
        return
    st.title("Quan ly nguoi dung")
    db = get_db()

    with st.expander("Them nguoi dung", expanded=False):
        with st.form("add_user_form"):
            c1, c2 = st.columns(2)
            username = c1.text_input("Ten dang nhap", key="add_uname")
            email = c2.text_input("Email", key="add_email")
            c3, c4 = st.columns(2)
            full_name = c3.text_input("Ho ten", key="add_fname")
            role = c4.selectbox("Vai tro", options=list(ROLES.keys()), format_func=lambda x: ROLES[x], key="add_role")
            password = st.text_input("Mat khau", type="password", key="add_pwd")
            if st.form_submit_button("Them nguoi dung", type="primary"):
                if username and email and password and full_name:
                    exist = db.query(User).filter((User.username == username) | (User.email == email)).first()
                    if exist: st.error("Ten dang nhap hoac email da ton tai")
                    else:
                        u = User(username=username, email=email, hashed_password=hash_password(password), full_name=full_name, role=role)
                        db.add(u); db.commit()
                        log_activity(db, "create", "user", f"Them user {username}")
                        st.success("Them thanh cong!"); st.rerun()

    users = db.query(User).order_by(User.created_at.desc()).all()
    if users:
        df = pd.DataFrame([{"ID": u.id, "Username": u.username, "Ho ten": u.full_name, "Email": u.email, "Vai tro": ROLES.get(u.role, u.role), "Hoat dong": "Co" if u.is_active else "Khong"} for u in users])
        st.dataframe(df, use_container_width=True, hide_index=True)
    db.close()


def checklist_page():
    st.title("Checklist mau")
    db = get_db()
    module = st.selectbox("Module", ["iqc", "oqc", "ipqc"], format_func=lambda x: x.upper())
    templates = db.query(ChecklistTemplate).filter(ChecklistTemplate.module == module).order_by(ChecklistTemplate.name).all()

    with st.expander("Tao checklist moi", expanded=False):
        with st.form("cl_form"):
            c1, c2 = st.columns(2)
            code = c1.text_input("Ma checklist")
            name = c2.text_input("Ten checklist")
            items_text = st.text_area("Danh sach muc kiem (moi dong: Ten | Tieu chuan | Min | Max)", height=150,
                placeholder="Do day | 2.0mm +/- 0.1 | 1.9 | 2.1\nDo rong | 1200mm +/- 2 | 1198 | 1202")
            if st.form_submit_button("Tao checklist", type="primary"):
                if code and name and items_text.strip():
                    items = []
                    for line in items_text.strip().split("\n"):
                        parts = [p.strip() for p in line.split("|")]
                        if parts and parts[0]:
                            items.append({
                                "item_name": parts[0],
                                "specification": parts[1] if len(parts) > 1 else "",
                                "standard_min": float(parts[2]) if len(parts) > 2 and parts[2] else None,
                                "standard_max": float(parts[3]) if len(parts) > 3 and parts[3] else None,
                            })
                    if items:
                        exist = db.query(ChecklistTemplate).filter(ChecklistTemplate.code == code).first()
                        if exist: st.error("Ma checklist da ton tai")
                        else:
                            db.add(ChecklistTemplate(code=code, name=name, module=module, items=items))
                            db.commit(); st.success("Tao thanh cong!"); st.rerun()

    if templates:
        for t in templates:
            with st.expander(f"{t.code} - {t.name} ({len(t.items or [])} muc)"):
                if t.items:
                    df = pd.DataFrame([{"Muc kiem": i.get("item_name",""), "Tieu chuan": i.get("specification",""), "Min": i.get("standard_min",""), "Max": i.get("standard_max","")} for i in t.items])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                if st.button("Xoa", key=f"del_cl_{t.id}"):
                    db.delete(t); db.commit(); st.rerun()
    else:
        st.info("Chua co checklist nao.")
    db.close()


def change_password():
    st.title("Doi mat khau")
    db = get_db()
    with st.form("change_pwd"):
        old = st.text_input("Mat khau cu", type="password")
        new = st.text_input("Mat khau moi", type="password")
        if st.form_submit_button("Doi mat khau", type="primary"):
            user = db.query(User).filter(User.id == st.session_state.user_id).first()
            if user and verify_password(old, user.hashed_password):
                user.hashed_password = hash_password(new)
                db.commit()
                st.success("Doi mat khau thanh cong!")
            else:
                st.error("Mat khau cu khong dung")
    db.close()


def main():
    if "user_id" not in st.session_state:
        login_page()
        return

    st.sidebar.title("Quality MES")
    st.sidebar.write(f"Xin chao: **{st.session_state.full_name}**")
    st.sidebar.caption(f"Vai tro: {ROLES.get(st.session_state.role, st.session_state.role)}")

    menu = st.sidebar.radio("Menu", [
        "🏠 Bang dieu khien",
        "📥 IQC - Kiem tra dau vao",
        "⚙️ IPQC - Kiem tra qua trinh",
        "📤 OQC - Kiem tra thanh pham",
        "⚠️ NCR + CAPA",
        "📊 SPC - Bao cao thong ke",
        "🔧 Thiet bi do",
        "📋 Checklist mau",
        "👥 Quan ly nguoi dung",
        "🔑 Doi mat khau",
        "🚪 Dang xuat",
    ])

    if menu == "🚪 Dang xuat":
        for key in ["user_id", "username", "full_name", "role"]:
            if key in st.session_state: del st.session_state[key]
        st.rerun()

    pages = {
        "🏠 Bang dieu khien": dashboard_page,
        "📥 IQC - Kiem tra dau vao": iqc_page,
        "⚙️ IPQC - Kiem tra qua trinh": ipqc_page,
        "📤 OQC - Kiem tra thanh pham": oqc_page,
        "⚠️ NCR + CAPA": ncr_page,
        "📊 SPC - Bao cao thong ke": spc_page,
        "🔧 Thiet bi do": equipment_page,
        "📋 Checklist mau": checklist_page,
        "👥 Quan ly nguoi dung": users_page,
        "🔑 Doi mat khau": change_password,
    }
    try:
        if menu in pages:
            pages[menu]()
    except Exception as e:
        st.error(f"Loi: {str(e)[:200]}")


if __name__ == "__main__":
    main()
