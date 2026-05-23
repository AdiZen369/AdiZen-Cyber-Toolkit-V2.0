# Installation Guide

Complete installation instructions for the AdiZenWorks Cybersecurity Toolkit V2.0.

## System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, Linux (Ubuntu 20.04+), macOS 10.15+
- **Python:** 3.8 or higher
- **RAM:** 4GB
- **Disk Space:** 500MB
- **Network:** Internet connection (for AI features and package installation)

### Recommended Requirements
- **Python:** 3.10+
- **RAM:** 8GB+
- **Network:** Stable broadband connection

## Installation Methods
### Method 1: Standard Installation (Recommended)

#### Step 1: Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
   ```cmd
   python --version

Linux (Ubuntu/Debian):
bash
sudo apt update
sudo apt install python3 python3-pip python3-tk

macOS:
bash
brew install python3

Step 2: Clone Repository
bash
git clone https://github.com/AdiZen369/AdiZen_Cybersecurity_Toolkit_V2.0.git
cd AdiZen_Cybersecurity_Toolkit_V2.0

Step 3: Install Dependencies
bash
pip install -r requirements.txt

Step 4: Verify Installation
bash
python -c "import flask, requests, bs4; print('All dependencies installed!')"

Method 2: Virtual Environment (Isolated Installation)
For a clean, isolated installation:

bash
# Create virtual environment
python -m venv venv


# Activate it
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

Method 3: Docker (Coming Soon)
Docker support is planned for V3.0

Configuration
Basic Configuration
Copy the example config and customize:

bash
cp config.example.json config.json
Edit config.json:

json
{
  "gemini_api_key": "YOUR_API_KEY_HERE",
  "app_settings": {
    "default_timeout": 10,
    "max_threads": 50,
    "enable_ai_analysis": true,
    "save_reports": true,
    "report_directory": "reports"
  }
}

AI Configuration (Optional)
To enable AI features:
Visit Google AI Studio
Sign in with your Google account
Create a new API key
Add the key to your config.json

Note: Gemini API is free for moderate use with rate limits.

Report Directory Setup
By default, reports are saved to reports/. 

To customize:
Edit config.json
Change report_directory to your preferred path
Ensure the directory exists and has write permissions

Verification
Test Web Dashboard
bash
cd web
python app.py
Visit http://localhost:5000 - you should see the dashboard.

Test Desktop App
bash
cd desktop
python main.py
The GUI window should open.

Test Tool Modules
bash
python -c "from src.adizenports import scan_ports; print('Tools loaded!')"

Troubleshooting Installation
Common Issues
Issue: "Python not found"
Solution:
Ensure Python is installed

On Windows, reinstall and check "Add to PATH"
Try python3 instead of python on Linux/macOS

Issue: "pip not found"
Solution:

bash
# Windows
python -m ensurepip --upgrade

# Linux
sudo apt install python3-pip
Issue: "Permission denied" on Linux/macOS
Solution:

bash
# Use --user flag
pip install --user -r requirements.txt

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
Issue: "Module 'tkinter' not found"
Solution:

bash
# Linux
sudo apt install python3-tk

# macOS - tkinter comes with Python

# Windows - reinstall Python with Tkinter component
Issue: Dependencies fail to install
Solution:

bash
# Upgrade pip first
python -m pip install --upgrade pip

# Try installing one by one
pip install flask
pip install requests
pip install beautifulsoup4
pip install google-generativeai
Platform-Specific Notes
Windows
Use Command Prompt or PowerShell as Administrator if needed

Antivirus may block some network scanning features

Windows Defender Firewall may prompt for permissions

Linux
Some features may require root privileges

Install build tools for certain packages:

bash
sudo apt install build-essential python3-dev

macOS
Install Xcode Command Line Tools if needed:
bash
xcode-select --install
Updating
To update to the latest version:

bash
git pull origin main
pip install --upgrade -r requirements.txt
Uninstallation
To completely remove the toolkit:

bash
# Remove virtual environment (if used)
rm -rf venv

# Remove the directory
cd ..
rm -rf adizenworks-cybersecurity-toolkit

# Uninstall packages (optional)
pip uninstall -r requirements.txt -y
Next Steps
Getting Started Guide

Tool Documentation

API Reference

Installation complete! Ready to start scanning? 🚀