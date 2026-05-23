# XSS Scanner

Cross-Site Scripting (XSS) vulnerability detection for web applications.

## Overview

The XSS Scanner tests web applications for Cross-Site Scripting vulnerabilities by injecting various payloads and analyzing responses. XSS is one of the most common web application vulnerabilities.

## What is XSS?

Cross-Site Scripting allows attackers to inject malicious scripts into web pages viewed by other users. This can lead to:

- Session hijacking
- Cookie theft
- Phishing attacks
- Defacement
- Malware distribution

## Usage

### Web Dashboard

1. Navigate to the "XSS Scanner" card
2. Enter target URL with a parameter (e.g., `?search=test`)
3. Click "Scan XSS"

### API Call

```bash
curl -X POST http://localhost:5000/api/scan/xss \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/search?q=test"}'
Python Module
python
from src.adizenxss import test_xss

result = test_xss('https://example.com/search?q=test')
print(result)
Payload Types
The scanner tests multiple XSS vectors:

Basic Script Injection:

xml
<script>alert('XSS')</script>
Event Handler:

xml
<img src=x onerror=alert('XSS')>
SVG-based:

xml
<svg onload=alert('XSS')>
Encoded Payloads:

xml
&#60;script&#62;alert('XSS')&#60;/script&#62;
Response Format
json
{
  "url": "https://example.com/search?q=test",
  "vulnerable": true,
  "payloads_tested": 12,
  "vulnerable_payloads": [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>"
  ],
  "risk_level": "HIGH",
  "recommendations": [
    "Implement input validation",
    "Use Content Security Policy",
    "Encode output properly"
  ],
  "scan_time": "2026-02-15T12:00:00"
}
Risk Levels
Level	Description	Action Required
CRITICAL	Multiple vulnerabilities, easy to exploit	Immediate patching
HIGH	Vulnerable to common payloads	Urgent fix needed
MEDIUM	Potential vulnerabilities detected	Investigate and fix
LOW	No vulnerabilities found	Continue monitoring
Remediation
Prevention Techniques
Input Validation:

python
# Whitelist allowed characters
allowed = set(string.ascii_letters + string.digits + ' ')
clean_input = ''.join(c for c in user_input if c in allowed)
Output Encoding:

python
# HTML escape special characters
import html
safe_output = html.escape(user_input)
Content Security Policy (CSP):

text
Content-Security-Policy: default-src 'self'; script-src 'self'
HTTPOnly Cookies:

text
Set-Cookie: session=abc123; HttpOnly; Secure
Framework-Specific Protection
Flask:

python
from flask import escape
output = escape(user_input)
Django:

python
from django.utils.html import escape
output = escape(user_input)
React:

jsx
// React automatically escapes by default
<div>{userInput}</div>
Security Considerations
⚠️ Warning:

XSS scanning can trigger security alerts

Some payloads may cause application errors

Always test on staging environments first

Never test production without authorization

Testing Checklist
✅ Authorization obtained in writing

✅ Staging environment available

✅ Incident response plan in place

✅ Backup available before testing

✅ Legal compliance verified

Advanced Techniques
Bypass Filters
Many applications attempt to filter XSS:

xml
<!-- Uppercase variation -->
<ScRiPt>alert('XSS')</sCrIpT>

<!-- Null bytes -->
<script\x00>alert('XSS')</script>

<!-- HTML entities -->
&lt;script&gt;alert('XSS')&lt;/script&gt;
Context-Specific Payloads
Different injection points require different payloads:

Inside HTML tags:

xml
" onload="alert('XSS')
Inside JavaScript:

javascript
'; alert('XSS'); //
Inside URLs:

text
javascript:alert('XSS')
False Positives
The scanner may report false positives when:

Input is echoed in HTML comments

Output is properly encoded but flagged

WAF/IDS blocks the payload

Always verify findings manually.

Limitations
Does not test stored/persistent XSS

Cannot bypass sophisticated WAFs

Limited to reflected XSS only

No DOM-based XSS detection

Related Tools
SQL Injection Tester - Test for SQLi vulnerabilities

Security Auditor - Check security headers

Header Inspector - Analyze HTTP headers

Test responsibly. Code securely. 🛡️