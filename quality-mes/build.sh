#!/bin/bash
set -e
echo "=== Installing Python packages ==="
pip install -r requirements.txt
echo "=== Building frontend ==="
cd frontend
npm install
npm run build
echo "=== Copying dist to backend/static ==="
mkdir -p ../backend/static
cp -r dist/* ../backend/static/
echo "=== Build complete ==="
