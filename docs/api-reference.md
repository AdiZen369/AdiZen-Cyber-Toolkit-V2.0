# API Reference

Complete API documentation for the AdiZenWorks Cybersecurity Toolkit V2.0 web dashboard.

## Base URL

http://localhost:5000/api

text

## Authentication

Currently, the API does not require authentication for local use. Authentication will be added in V3.0 for the cloud-hosted version.

## Response Format

All API responses are in JSON format:

```json
{
  "status": "success|error",
  "data": {},
  "error": "Error message (if applicable)",
  "timestamp": "ISO 8601 timestamp"
}
Rate Limiting
No rate limiting for local installations. Cloud version (V3.0) will implement rate limiting.

Scanning Tools
Port Scanner
Endpoint: POST /api/scan/ports

Description: Scan TCP ports on a target host

Request Body:

json
{
  "target": "scanme.nmap.org",
  "port_range": "20-1000"
}
Response:

json
{
  "target": "scanme.nmap.org",
  "ip": "45.33.32.156",
  "ports": "20-1000",
  "open_ports":,[1]
  "total_scanned": 981,
  "scan_time": "2026-02-15T12:00:00"
}
Security Auditor
Endpoint: POST /api/scan/security

Description: Audit HTTP security headers

Request Body:

json
{
  "url": "https://example.com"
}
Response:

json
{
  "url": "https://example.com",
  "score": 80,
  "security_headers": {
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'self'"
  },
  "missing_headers": ["Strict-Transport-Security"],
  "status_code": 200,
  "scan_time": "2026-02-15T12:00:00"
}
XSS Scanner
Endpoint: POST /api/scan/xss

Description: Test for XSS vulnerabilities

Request Body:

json
{
  "url": "https://example.com/search?q=test"
}
Response:

json
{
  "url": "https://example.com/search?q=test",
  "vulnerable": false,
  "payloads_tested": 12,
  "vulnerable_payloads": [],
  "risk_level": "LOW",
  "scan_time": "2026-02-15T12:00:00"
}
SQL Injection Tester
Endpoint: POST /api/scan/sqli

Description: Test for SQL injection vulnerabilities

Request Body:

json
{
  "url": "https://example.com/product?id=1"
}
Response:

json
{
  "url": "https://example.com/product?id=1",
  "vulnerable": false,
  "payloads_tested": 8,
  "vulnerable_payloads": [],
  "risk_level": "LOW",
  "scan_time": "2026-02-15T12:00:00"
}
Web Spider
Endpoint: POST /api/scan/spider

Description: Crawl website and extract links

Request Body:

json
{
  "url": "https://example.com",
  "max_pages": 10
}
Response:

json
{
  "start_url": "https://example.com",
  "pages_crawled": ["https://example.com", "https://example.com/about"],
  "links_found": ["https://example.com/contact", "https://example.com/products"],
  "total_pages": 10,
  "total_links": 45,
  "scan_time": "2026-02-15T12:00:00"
}
Network Mapper
Endpoint: POST /api/scan/network

Description: Scan network and discover devices

Request Body:

json
{
  "network": "192.168.1.0/24"
}
Response:

json
{
  "network": "192.168.1.0/24",
  "hosts_found": 5,
  "devices": [
    {
      "ip": "192.168.1.1",
      "hostname": "router.local",
      "open_ports": ,
      "device_type": "Network Device",
      "risk_level": "MEDIUM"
    }
  ],
  "scan_time": 45.2
}
Utility Tools
Hash Generator
Endpoint: POST /api/tool/hash

Description: Generate cryptographic hash

Request Body:

json
{
  "text": "AdiZenWorks2026",
  "algorithm": "sha256"
}
Supported Algorithms: md5, sha1, sha256, sha512

Response:

json
{
  "input_text": "AdiZenWorks2026",
  "algorithm": "sha256",
  "hash": "abc123...",
  "hash_length": 64,
  "timestamp": "2026-02-15T12:00:00"
}
Header Inspector
Endpoint: POST /api/tool/headers

Description: Inspect HTTP headers

Request Body:

json
{
  "url": "https://example.com"
}
Response:

json
{
  "url": "https://example.com",
  "status_code": 200,
  "headers": {
    "Server": "nginx",
    "Content-Type": "text/html",
    "X-Frame-Options": "DENY"
  },
  "total_headers": 15,
  "scan_time": "2026-02-15T12:00:00"
}
AI Assistant
Ask AI
Endpoint: POST /api/ai/ask

Description: Get AI-powered security advice

Request Body:

json
{
  "question": "What are the top 3 security headers every website should have?"
}
Response:

json
{
  "question": "What are the top 3 security headers every website should have?",
  "answer": "The top 3 security headers are: 1. Strict-Transport-Security (HSTS)...",
  "status": "success",
  "timestamp": "2026-02-15T12:00:00"
}
Note: Requires Gemini API key configured in config.json

Error Responses
400 Bad Request
json
{
  "error": "Target is required"
}
404 Not Found
json
{
  "error": "Endpoint not found"
}
500 Internal Server Error
json
{
  "error": "Internal server error"
}
Integration Examples
Python
python
import requests

response = requests.post(
    'http://localhost:5000/api/scan/ports',
    json={'target': 'scanme.nmap.org', 'port_range': '20-100'}
)
print(response.json())
JavaScript (Fetch)
javascript
fetch('http://localhost:5000/api/scan/ports', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        target: 'scanme.nmap.org',
        port_range: '20-100'
    })
})
.then(res => res.json())
.then(data => console.log(data));
cURL
bash
curl -X POST http://localhost:5000/api/scan/ports \
  -H "Content-Type: application/json" \
  -d '{"target":"scanme.nmap.org","port_range":"20-100"}'
Need more help? Check out the Getting Started Guide!