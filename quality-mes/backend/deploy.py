import os
import socket
import uvicorn

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"


if __name__ == "__main__":
    ip = get_local_ip()
    print("=" * 60)
    print("  Quality MES - He thong quan ly chat luong")
    print("=" * 60)
    print()
    print(f"  May chu:     http://{ip}:8000")
    print(f"  API Docs:    http://{ip}:8000/api/docs")
    print()
    print("  Tai khoan mac dinh:")
    print("    admin       / Admin123   (Quan ly)")
    print("    qc_manager  / Qc123456   (Truong QC)")
    print("    inspector1  / Insp123456 (Kiem tra vien)")
    print()
    print("  Chia se link nay cho team QC de truy cap.")
    print("  Bam Ctrl+C de dung may chu.")
    print("=" * 60)
    print()

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="warning",
    )
