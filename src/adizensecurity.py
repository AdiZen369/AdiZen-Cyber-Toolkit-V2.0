#!/usr/bin/env python3
"""
AdiZenWorks Security Auditor
HTTP security headers analysis tool
Company: AdiZenWorks Inc.
"""

import requests
from datetime import datetime

def audit_security(url):
    """
    Audit HTTP security headers
    
    Args:
        url: website URL to audit
    
    Returns:
        dict with security score and findings
    """
    results = {
        "url": url,
        "score": 0,
        "headers_found": [],
        "scan_time": datetime.now().isoformat()
    }
    
    # Security headers to check
    security_headers = {
        "X-Frame-Options": "Clickjacking protection",
        "X-Content-Type-Options": "MIME-sniffing protection",
        "Strict-Transport-Security": "HTTPS enforcement",
        "Content-Security-Policy": "XSS protection",
        "X-XSS-Protection": "XSS filter"
    }
    
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        
        # Store all headers
        results["headers_found"] = list(response.headers.keys())
        
        # Check security headers
        found_headers = {}
        for header, description in security_headers.items():
            if header in response.headers:
                results["score"] += 20
                found_headers[header] = response.headers[header]
        
        results["security_headers"] = found_headers
        results["missing_headers"] = [h for h in security_headers.keys() 
                                      if h not in response.headers]
        results["status_code"] = response.status_code
        
    except requests.RequestException as e:
        results["error"] = str(e)
    
    return results

if __name__ == "__main__":
    # Test
    print("AdiZenWorks Security Auditor Test")
    print("-" * 40)
    results = audit_security("https://example.com")
    print(f"URL: {results['url']}")
    print(f"Security Score: {results['score']}/100")
    print(f"Missing: {results.get('missing_headers', [])}")
