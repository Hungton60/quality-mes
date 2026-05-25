#!/bin/bash
set -e
echo "=== Installing Python packages ==="
pip install -r quality-mes/requirements.txt
echo "=== Building frontend ==="
cd quality-mes/frontend
npm install
npm run build
echo "=== Build complete ==="
