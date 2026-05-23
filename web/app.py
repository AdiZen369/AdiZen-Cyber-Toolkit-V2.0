#!/usr/bin/env python3
"""
AdiZen Cybersecurity Toolkit - Web Interface
Flask web application for security tools
Company: AdiZenWorks Inc.
"""

import sys
import os
from flask import Flask, render_template, request, jsonify
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import adizenports
import adizenheaders
import adizenhash
import adizenai
import adizenxss
import adizensqli
import adizenmapper
import adizenspider
import adizendns
import adizenssl
import adizenpassword
import adizensubdomain
import adizencve
import adizenrevshell
import adizensecurity

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me-in-production')

# Initialize AI Assistant
ai = adizenai.AdiZenAI()


@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')


# PORT SCANNER
@app.route('/api/port-scan', methods=['POST'])
def port_scan():
    """Port scanning endpoint"""
    data = request.json
    target = data.get('target', '')
    port_range = data.get('ports', '1-1000')

    try:
        results = adizenports.scan_ports(target, port_range)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# SECURITY HEADERS
@app.route('/api/check-headers', methods=['POST'])
def check_headers():
    """Security headers check endpoint"""
    data = request.json
    url = data.get('url', '')

    try:
        results = adizenheaders.inspect_headers(url)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# HASH GENERATOR
@app.route('/api/generate-hash', methods=['POST'])
def hash_generate():
    """Hash generation endpoint"""
    data = request.json
    text = data.get('text', '')
    algorithm = data.get('algorithm', 'sha256')

    try:
        results = adizenhash.generate_hash(text, algorithm)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# XSS SCANNER
@app.route('/api/xss-scan', methods=['POST'])
def xss_scan():
    """XSS scanning endpoint"""
    data = request.json
    url = data.get('url', '')

    try:
        results = adizenxss.scan_xss(url)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# SQL INJECTION SCANNER
@app.route('/api/sqli-scan', methods=['POST'])
def sqli_scan():
    """SQL Injection scanning endpoint"""
    data = request.json
    url = data.get('url', '')

    try:
        results = adizensqli.scan_sqli(url)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# NETWORK MAPPER
@app.route('/api/network-map', methods=['POST'])
def network_map():
    """Network mapping endpoint"""
    data = request.json
    target = data.get('target', '')

    try:
        results = adizenmapper.map_network(target)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# WEB SPIDER
@app.route('/api/web-spider', methods=['POST'])
@app.route('/api/spider', methods=['POST'])
def web_spider():
    """Web spidering endpoint"""
    data = request.json
    url = data.get('url', '')
    max_depth = data.get('depth', 2)

    try:
        results = adizenspider.spider_website(url, max_depth)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# AI ASSISTANT
@app.route('/api/ai-assistant', methods=['POST'])
@app.route('/api/ai-analyze', methods=['POST'])
def ai_assistant():
    """AI Assistant / Analyze endpoint"""
    data = request.json
    question = data.get('question', '') or data.get('prompt', '')
    context = data.get('context', '')

    # Support BYOK config from frontend
    provider = data.get('provider')
    model = data.get('model')
    api_key = data.get('api_key')
    base_url = data.get('base_url')

    try:
        full_prompt = question
        if context:
            full_prompt = f"{question}\n\nContext:\n{context}"

        if api_key:
            ai_instance = adizenai.AdiZenAI(api_key=api_key)
            results = ai_instance.get_security_advice(full_prompt)
        else:
            results = ai.get_security_advice(full_prompt)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# AI CONNECTION TEST
@app.route('/api/ai-test', methods=['POST'])
def ai_test():
    """Test AI provider connection"""
    data = request.json
    try:
        api_key = data.get('api_key')
        ai_instance = adizenai.AdiZenAI(api_key=api_key) if api_key else ai
        result = ai_instance.get_security_advice("Test: respond with 'Connection OK'")
        return jsonify({"ok": True, "response": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


# DNS LOOKUP
@app.route('/api/dns-lookup', methods=['POST'])
def dns_lookup():
    """DNS lookup endpoint"""
    data = request.json
    domain = data.get('domain', '')

    try:
        results = adizendns.dns_lookup(domain)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# SSL INSPECTOR
@app.route('/api/ssl-inspect', methods=['POST'])
def ssl_inspect():
    """SSL/TLS inspection endpoint"""
    data = request.json
    hostname = data.get('hostname', '')
    port = data.get('port', 443)

    try:
        results = adizenssl.inspect_ssl(hostname, port)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# PASSWORD STRENGTH
@app.route('/api/password-check', methods=['POST'])
def password_check():
    """Password strength analysis endpoint"""
    data = request.json
    password = data.get('password', '')

    try:
        results = adizenpassword.analyze_password(password)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# SUBDOMAIN ENUMERATOR
@app.route('/api/subdomain-enum', methods=['POST'])
def subdomain_enum():
    """Subdomain enumeration endpoint"""
    data = request.json
    domain = data.get('domain', '')

    try:
        results = adizensubdomain.enumerate_subdomains(domain)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# CVE SEARCH
@app.route('/api/cve-search', methods=['POST'])
def cve_search():
    """CVE search endpoint"""
    data = request.json
    query = data.get('query', '')
    max_results = data.get('max_results', 10)

    try:
        results = adizencve.search_cve(query, max_results)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# REVERSE SHELL DETECTOR
@app.route('/api/revshell-detect', methods=['POST'])
def revshell_detect():
    """Reverse shell detection endpoint"""
    data = request.json
    text = data.get('text', '')

    try:
        results = adizenrevshell.detect_reverse_shells(text)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# SECURITY AUDIT
@app.route('/api/security-audit', methods=['POST'])
def security_audit():
    """Full security audit endpoint"""
    data = request.json
    url = data.get('url', '')

    try:
        results = adizensecurity.audit_security(url)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "app": "AdiZen Cybersecurity Toolkit",
        "version": "2.0"
    })


if __name__ == '__main__':
    print("[*] AdiZenWorks Web Interface starting...")
    print("[*] Open http://localhost:5000 in your browser")
    app.run(debug=False, host='0.0.0.0', port=5000)
