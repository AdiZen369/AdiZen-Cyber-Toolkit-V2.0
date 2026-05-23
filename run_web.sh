#!/bin/bash
echo "======================================"
echo " AdiZenWorks Web Interface"
echo " http://localhost:5000"
echo "======================================"
cd "$(dirname "$0")"
pip install -r requirements.txt -q
python3 web/app.py
