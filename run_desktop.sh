#!/bin/bash
echo "======================================"
echo " AdiZenWorks Cybersecurity Toolkit V2"
echo " Desktop GUI Launcher"
echo "======================================"
cd "$(dirname "$0")"
pip install -r requirements.txt -q
python3 desktop/main.py
