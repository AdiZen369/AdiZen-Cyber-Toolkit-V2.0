#!/usr/bin/env python3
"""
AdiZenWorks Header Inspector
HTTP header analysis tool
Company: AdiZenWorks Inc.
"""

import requests
import urllib3
from datetime import datetime

# Suppress InsecureRequestWarning when verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from typing import Dict


class AdiZenHeaders:
    """HTTP header analyzer class"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def analyze_url(self, url: str) -> Dict:
        """
        Analyze HTTP security headers
        
        Args:
            url: website URL to inspect
        
        Returns:
            dict with header analysis including security score
        """
        results = {
            "url": url,
            "headers": {},
            "security_score": 0,
            "missing_headers": [],
            "present_headers": [],
            "scan_time": datetime.now().isoformat()
        }
        
        try:
            response = requests.get(url, timeout=self.timeout, allow_redirects=True, verify=False)
            
            # Store all headers
            results["headers"] = dict(response.headers)
            results["status_code"] = response.status_code
            results["final_url"] = response.url
            
            # Critical security headers to check
            security_headers = {
                "Strict-Transport-Security": "HSTS",
                "Content-Security-Policy": "CSP",
                "X-Frame-Options": "Clickjacking Protection",
                "X-Content-Type-Options": "MIME Sniffing Protection",
                "X-XSS-Protection": "XSS Filter",
                "Referrer-Policy": "Referrer Policy",
                "Permissions-Policy": "Permissions Policy"
            }
            
            # Check which headers are present
            for header, description in security_headers.items():
                if header in response.headers:
                    results["present_headers"].append(f"{description} ({header})")
                else:
                    results["missing_headers"].append(f"{description} ({header})")
            
            # Calculate security score (each header worth ~14 points)
            results["security_score"] = int((len(results["present_headers"]) / len(security_headers)) * 100)
            
            # Additional analysis
            results["server"] = response.headers.get("Server", "Not disclosed")
            results["content_type"] = response.headers.get("Content-Type", "Unknown")
            results["total_headers"] = len(response.headers)
            
        except requests.RequestException as e:
            results["error"] = str(e)
            results["security_score"] = 0
        
        return results


# Keep backward compatibility
def inspect_headers(url):
    """
    Legacy function for backward compatibility
    
    Args:
        url: website URL to inspect
    
    Returns:
        dict with header analysis
    """
    results = {
        "url": url,
        "headers": {},
        "scan_time": datetime.now().isoformat()
    }
    
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        
        # Store all headers
        results["headers"] = dict(response.headers)
        results["status_code"] = response.status_code
        results["final_url"] = response.url
        
        # Analyze important headers
        analysis = {}
        
        # Server information
        if "Server" in response.headers:
            analysis["server"] = response.headers["Server"]
        
        # Content type
        if "Content-Type" in response.headers:
            analysis["content_type"] = response.headers["Content-Type"]
        
        # Security headers
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "X-XSS-Protection"
        ]
        
        found_security = [h for h in security_headers if h in response.headers]
        analysis["security_headers_found"] = found_security
        analysis["security_score"] = len(found_security) * 20
        
        results["analysis"] = analysis
        results["total_headers"] = len(response.headers)
    
    except requests.RequestException as e:
        results["error"] = str(e)
    
    return results


if __name__ == "__main__":
    # Test
    print("AdiZenWorks Header Inspector Test")
    print("-" * 40)
    
    analyzer = AdiZenHeaders()
    results = analyzer.analyze_url("https://example.com")
    
    print(f"URL: {results['url']}")
    print(f"Status: {results.get('status_code')}")
    print(f"Security Score: {results['security_score']}/100")
    print(f"\nPresent Headers: {len(results['present_headers'])}")
    print(f"Missing Headers: {len(results['missing_headers'])}")
