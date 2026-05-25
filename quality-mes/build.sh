#!/bin/bash
set -e
echo "=== Installing Python packages ==="
pip install -r requirements.txt
echo "=== Building frontend ==="
cd frontend
npm install
npm run build
echo "=== Copying dist to static ==="
mkdir -p ../static
cp -r dist/* ../static/
echo "=== Build complete ==="
