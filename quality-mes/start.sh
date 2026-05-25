#!/bin/bash
echo "=== Starting Quality MES ==="
echo "Current dir: $(pwd)"
echo "Python: $(python --version)"
cd backend
echo "Backend dir: $(pwd)"
echo "Files in app/: $(ls app/ 2>/dev/null || echo 'ERROR')"
echo "Trying import..."
python -c "from app.main import app; print('Import OK')" 2>&1
if [ $? -ne 0 ]; then
    echo "IMPORT FAILED"
    exit 1
fi
echo "=== Starting uvicorn ==="
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level debug
