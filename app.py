#!/usr/bin/env python3
"""
AdiZenWorks Cybersecurity Toolkit - Web Application (Root Entry Point)
Flask-based web interface for all security tools
Company: AdiZenWorks Inc.
Version: 2.0 Web
"""

import sys
import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from datetime import datetime
from pathlib import Path
import json

# Add src/ to path so modules can be imported from any working directory
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import all tool modules
import adizenports
import adizensecurity
import adizenspider
import adizensqli
import adizenxss
import adizenmapper
import adizenhash
import adizenheaders
import adizenai

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-in-production')

# Reports directory
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/api/scan/ports', methods=['POST'])
def scan_ports():
    """Port scanning endpoint"""
    data = request.json
    target = data.get('target')
    ports = data.get('ports', '20-100')
    results = adizenports.scan_ports(target, ports)
    save_report('port_scanner', results)
    return jsonify(results)


@app.route('/api/scan/security', methods=['POST'])
def scan_security():
    """Security audit endpoint"""
    data = request.json
    url = data.get('url')
    results = adizensecurity.audit_security(url)
    save_report('security_auditor', results)
    return jsonify(results)


@app.route('/api/scan/spider', methods=['POST'])
def scan_spider():
    """Web spider endpoint"""
    data = request.json
    url = data.get('url')
    max_pages = data.get('max_pages', 10)
    results = adizenspider.spider_website(url, max_pages)
    save_report('web_spider', results)
    return jsonify(results)


@app.route('/api/scan/sqli', methods=['POST'])
def scan_sqli():
    """SQL injection test endpoint"""
    data = request.json
    url = data.get('url')
    results = adizensqli.scan_sqli(url)
    save_report('sqli_tester', results)
    return jsonify(results)


@app.route('/api/scan/xss', methods=['POST'])
def scan_xss():
    """XSS scanner endpoint"""
    data = request.json
    url = data.get('url')
    results = adizenxss.scan_xss(url)
    save_report('xss_scanner', results)
    return jsonify(results)


@app.route('/api/scan/network', methods=['POST'])
def scan_network():
    """Network mapping endpoint"""
    data = request.json
    network = data.get('network')
    results = adizenmapper.map_network(network)
    save_report('network_mapper', results)
    return jsonify(results)


@app.route('/api/tools/hash', methods=['POST'])
def generate_hash():
    """Hash generation endpoint"""
    data = request.json
    text = data.get('text')
    algorithm = data.get('algorithm', 'sha256')
    results = adizenhash.generate_hash(text, algorithm)
    save_report('hash_generator', results)
    return jsonify(results)


@app.route('/api/scan/headers', methods=['POST'])
def scan_headers():
    """Header inspection endpoint"""
    data = request.json
    url = data.get('url')
    results = adizenheaders.inspect_headers(url)
    save_report('header_inspector', results)
    return jsonify(results)


@app.route('/api/ai/analyze', methods=['POST'])
def ai_analyze():
    """AI analysis endpoint"""
    data = request.json
    query_type = data.get('type', 'advice')
    query_data = data.get('data', '')
    results = adizenai.analyze_with_ai(query_type, query_data)
    save_report('ai_assistant', results)
    return jsonify(results)


@app.route('/api/reports')
def list_reports():
    """List all saved reports"""
    reports = []
    for report_file in REPORTS_DIR.glob('*.json'):
        reports.append({
            'filename': report_file.name,
            'timestamp': report_file.stat().st_mtime
        })
    reports.sort(key=lambda x: x['timestamp'], reverse=True)
    return jsonify(reports[:50])


@app.route('/api/reports/<filename>')
def get_report(filename):
    """Get specific report"""
    report_path = REPORTS_DIR / filename
    if report_path.exists():
        with open(report_path) as f:
            return jsonify(json.load(f))
    return jsonify({'error': 'Report not found'}), 404


@app.route('/downloads/<filename>')
def download_report(filename):
    """Download report file"""
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)


@app.route('/health')
def health():
    """Health check"""
    return jsonify({"status": "healthy", "version": "2.0"})


def save_report(tool_name, results):
    """Save scan report to file"""
    report = {
        "tool": tool_name,
        "company": "AdiZenWorks Inc.",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "data": results
    }
    filename = f"adizen_{tool_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(REPORTS_DIR / filename, 'w') as f:
        json.dump(report, f, indent=2)
    return filename


if __name__ == '__main__':
    print("=" * 60)
    print("🛡️  AdiZenWorks Cybersecurity Toolkit V2.0 - Web Edition")
    print("=" * 60)
    print("Access at: http://localhost:5000")
    print("=" * 60)
    app.run(debug=False, host='127.0.0.1', port=5000)
