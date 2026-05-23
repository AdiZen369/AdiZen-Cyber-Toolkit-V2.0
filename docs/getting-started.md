# Getting Started with AdiZenWorks Cybersecurity Toolkit

Welcome to the AdiZenWorks Cybersecurity Toolkit V2.0! This guide will help you get up and running quickly.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Git** (for cloning the repository)
- **Internet connection** (for AI features)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/AdiZen369/adizenworks_cybersecurity_toolkit_V2.0.git
cd adizenworks_cybersecurity_toolkit_V2.0

2. Install Dependencies
bash
pip install -r requirements.txt
3. Configure AI Assistant (Optional)
The toolkit includes AI-powered analysis using Google Gemini. To enable this feature:

Get a free API key from Google AI Studio

Copy the example config:

bash
cp config.example.json config.json
Edit config.json and add your API key:

json
{
  "gemini_api_key": "YOUR_API_KEY_HERE"
}

Running the Application

Web Dashboard (Recommended)
The web dashboard provides a modern, browser-based interface:

Windows:
START_WEB_APP.bat

Linux/macOS:
bash
cd web
python app.py

Then open your browser to: http://localhost:5000

Desktop Application
For a native Windows GUI experience:

Windows:
START_DESKTOP_APP.bat

Linux/macOS:
bash
cd desktop
python main.py

First Scan
Let's run your first security scan:

Port Scan Example:
Target: scanme.nmap.org
Port Range: 20-100
Click "Start Scan"

Security Audit Example:
URL: https://example.com
Click "Audit Security"

Understanding Results
All scan results are displayed in JSON format and include:

Timestamp - When the scan was performed
Target - The system/URL that was scanned
Results - Detailed findings
Risk Assessment - Severity ratings where applicable
Results are also saved to the reports/ directory for future reference.

Safety & Ethics
⚠️ IMPORTANT: This toolkit is for authorized security testing only.

Legal Use:

✅ Your own systems and networks
✅ Systems where you have explicit written permission
✅ Educational purposes in controlled environments
✅ Professional penetration testing with proper authorization

Illegal Use:

❌ Unauthorized system access
❌ Testing without permission
❌ Malicious activities
❌ Any activities that violate laws or regulations

Always obtain written authorization before testing any system you don't own.

Troubleshooting
"Module not found" errors
bash
pip install --upgrade -r requirements.txt
Web dashboard won't start
Check if port 5000 is already in use
Try a different port by editing web/app.py
Ensure Flask is installed: pip install flask

AI features not working
Verify your API key in config.json

Check internet connection
Ensure google-generativeai is installed
API keys are free but have rate limits

Permission errors on Windows
Run the application as Administrator if you encounter permission issues.

Next Steps
Read the Tool Documentation to learn about each security tool
Check out the API Reference for integration options

Join our community and contribute to the project

Support
Need help? Here's how to get support:

Issues: Open an issue on GitHub Issues
Email: security@adizenworks.com
Documentation: Read the full docs in the docs/ directory
Ready to secure your digital future? Let's get scanning! 🔒