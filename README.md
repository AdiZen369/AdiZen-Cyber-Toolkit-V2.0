<div align="center">

# 🔒 AdiZenWorks Cybersecurity Toolkit V2.0

[![License: MIT](https://img.shields.io/badge/License-MIT-crimson.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/AdiZen369/AdiZen-Cyber-Toolkit-V2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**Professional Security Testing Suite for Ethical Hackers & Security Researchers**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

![Demo](docs/screenshots/demo.gif)
*Complete security toolkit with Desktop GUI and Web Dashboard*

</div>

---

## 🎯 Overview

AdiZenWorks Cybersecurity Toolkit V2.0 is a comprehensive security testing suite designed for penetration testers, security researchers, and IT professionals. Built with Python and powered by AI, it provides both a desktop application and web-based dashboard for conducting security assessments.

### ⚠️ Ethical Use Only
This toolkit is designed for **authorized security testing only**. Users must obtain explicit written permission before testing any systems they do not own. Unauthorized access is illegal and unethical.

---

## ✨ Features

### 🛠️ 8 Professional Security Tools

| Tool | Description | Use Case |
|------|-------------|----------|
| **Port Scanner** | Fast TCP port scanning (1-65535) | Network reconnaissance |
| **Security Auditor** | HTTP security headers analysis | Web app security assessment |
| **Web Spider** | Website crawler & link extractor | Content discovery |
| **SQL Injection Tester** | Automated SQLi vulnerability detection | Database security testing |
| **XSS Scanner** | Cross-site scripting detection | Web app vulnerability assessment |
| **Network Mapper** | Subnet scanning & device discovery | Network topology mapping |
| **Hash Generator** | Multi-algorithm hash generation | Cryptographic operations |
| **Header Inspector** | Detailed HTTP header analysis | Server fingerprinting |

### 🤖 AI-Powered Analysis
- **Google Gemini Integration** for intelligent vulnerability analysis
- Automated risk assessment and prioritization
- AI-generated remediation recommendations
- Natural language security advice

### 💻 Dual Interface
- **Desktop Application** - Native Windows GUI built with Tkinter
- **Web Dashboard** - Modern Flask-based interface with real-time updates

### 📊 Professional Reporting
- JSON export for all scan results
- Timestamped reports with unique identifiers
- Structured data for integration with other tools
- Audit trail for compliance requirements

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for AI features)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AdiZen369/AdiZen-Cyber-Toolkit-V2.0.git
cd adizenworks-cybersecurity-toolkit_V2.0
Install dependencies

bash
pip install -r requirements.txt
Configure AI (Optional)

bash
# Get free API key from https://makersuite.google.com/app/apikey
cp config.example.json config.json
# Edit config.json and add your Gemini API key

Running the Application
Desktop Application:

bash
# Windows
START_DESKTOP_APP.bat

# Linux/macOS
python desktop/main.py

Web Dashboard:

bash
# Windows
START_WEB_APP.bat

# Linux/macOS
python web/app.py

The web dashboard will be available at http://localhost:5000

📁 Project Structure
text
adizenworks-cybersecurity-toolkit/
├── src/                    # Core security tool modules
│   ├── adizenai.py        # AI assistant integration
│   ├── adizenhash.py      # Hash generator
│   ├── adizenheaders.py   # Header inspector
│   ├── adizenmapper.py    # Network mapper
│   ├── adizenports.py     # Port scanner
│   ├── adizensecurity.py  # Security auditor
│   ├── adizenspider.py    # Web spider
│   ├── adizensqli.py      # SQL injection tester
│   └── adizenxss.py       # XSS scanner
├── desktop/               # Desktop application
│   └── main.py           # Tkinter GUI
├── web/                  # Web dashboard
│   ├── app.py           # Flask application
│   ├── static/          # CSS, JS, assets
│   └── templates/       # HTML templates
├── docs/                # Documentation
├── tests/               # Unit tests
├── reports/             # Scan results (gitignored)
└── README.md           # This file

📖 Documentation

Getting Started Guide
Installation Instructions
Tool Documentation
API Reference

🎨 Screenshots
Web Dashboard
Web Dashboard-Screenshot

Desktop Application
Desktop App-Screenshot

Scan Results
Results-Screenshot


🛡️ Security & Privacy
All scanning is performed locally on your machine
No data is sent to external services (except optional AI analysis)
Scan results are stored locally in reports/directory
Open-source code - audit it yourself!

🗺️ Roadmap
V2.0 (Current) ✅
8 security tools
Desktop & Web interfaces
AI-powered analysis
JSON report generation

V3.0 (Planned) 🚀
Mobile applications (iOS & Android)
Cloud-hosted SaaS version
Advanced analytics dashboard
Multi-user collaboration
REST API for integrations
Automated remediation suggestions

🤝 Contributing
We welcome contributions! Please see CONTRIBUTING.md for guidelines.
Ways to Contribute
🐛 Report bugs
💡 Suggest new features
📝 Improve documentation
🔧 Submit pull requests
⭐ Star the project

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

Terms of Use
✅ Authorized security testing only
✅ Educational purposes
✅ Personal research
❌ Unauthorized system access
❌ Malicious activities
❌ Illegal use

By using this software, you agree to use it ethically and legally.

🏢 About AdiZenWorks
AdiZenWorks Inc. - Securing Your Digital Future

Founded by cybersecurity professional, AdiZenWorks develops cutting-edge security tools for ethical hackers and IT professionals worldwide.

🌐 Website: www.adizenworks.com (coming soon)
📧 Contact: security@adizenworks.com
🐦 Twitter: @AdiZenWorks

💖 Support
If you find this toolkit useful:
⭐ Star the repository
🍴 Fork and contribute
📢 Share with the security community
🐛 Report issues

📊 Stats
GitHub stars
GitHub forks
GitHub issues

<div align="center">
Built with ❤️ by AdiZenWorks
© 2026 AdiZenWorks Inc. All Rights Reserved.