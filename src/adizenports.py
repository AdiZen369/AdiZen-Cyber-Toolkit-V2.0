#!/usr/bin/env python3
"""
AdiZenWorks Port Scanner
Simple network port scanning tool
Company: AdiZenWorks Inc.
"""

import socket
from datetime import datetime
from typing import List, Dict


class AdiZenPorts:
    """Port scanner class"""
    
    def __init__(self, timeout: int = 1):
        self.timeout = timeout
    
    def scan_target(self, target: str, ports: List[int]) -> List[Dict]:
        """
        Scan ports on target host
        
        Args:
            target: hostname or IP address
            ports: list of port numbers to scan
        
        Returns:
            list of dicts with scan results
        """
        results = []
        
        try:
            # Resolve hostname to IP
            target_ip = socket.gethostbyname(target)
        except socket.gaierror:
            return [{'error': f'Could not resolve hostname: {target}'}]
        
        # Common service mapping
        services = {
            20: 'FTP-DATA', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 
            25: 'SMTP', 53: 'DNS', 80: 'HTTP', 110: 'POP3',
            143: 'IMAP', 443: 'HTTPS', 3306: 'MySQL', 3389: 'RDP',
            5432: 'PostgreSQL', 8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt'
        }
        
        # Scan each port
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            result = sock.connect_ex((target_ip, port))
            
            status = 'open' if result == 0 else 'closed'
            
            results.append({
                'port': port,
                'status': status,
                'service': services.get(port, 'Unknown') if status == 'open' else None
            })
            
            sock.close()
        
        return results


# Keep backward compatibility
def scan_ports(target, port_range):
    """
    Legacy function for backward compatibility
    
    Args:
        target: hostname or IP address
        port_range: string like "20-100" or single port "80"
    
    Returns:
        dict with scan results
    """
    results = {
        "target": target,
        "ports": port_range,
        "open_ports": [],
        "scan_time": datetime.now().isoformat()
    }
    
    try:
        # Parse port range
        if '-' in port_range:
            start, end = map(int, port_range.split('-'))
        else:
            start = end = int(port_range)
        
        # Resolve hostname to IP
        try:
            target_ip = socket.gethostbyname(target)
            results["ip"] = target_ip
        except socket.gaierror:
            results["error"] = f"Could not resolve hostname: {target}"
            return results
        
        # Scan ports
        for port in range(start, end + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                results["open_ports"].append(port)
            
            sock.close()
        
        results["total_scanned"] = end - start + 1
        
    except Exception as e:
        results["error"] = str(e)
    
    return results


if __name__ == "__main__":
    # Test
    print("AdiZenWorks Port Scanner Test")
    print("-" * 40)
    
    scanner = AdiZenPorts()
    results = scanner.scan_target("scanme.nmap.org", list(range(20, 101)))
    
    print(f"Scan complete!")
    for r in results:
        if r['status'] == 'open':
            print(f"Port {r['port']}: {r['status']} - {r['service']}")
