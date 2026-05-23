"""
AdiZen Network Mapper - Asset Discovery & Network Reconnaissance
Author: AdiZenWorks Inc.
License: MIT
"""

import socket
import subprocess
import platform
import concurrent.futures
from typing import List, Dict, Optional
import ipaddress

class AdiZenMapper:
    """Network mapping and asset discovery tool"""
    
    def __init__(self, timeout: int = 2):
        self.timeout = timeout
        self.discovered_hosts = []
    
    def ping_host(self, ip: str) -> Dict[str, any]:
        """
        Ping a single host to check if it's alive
        
        Args:
            ip: IP address to ping
            
        Returns:
            Dict with host status and response time
        """
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-w' if platform.system().lower() == 'windows' else '-W', str(self.timeout), ip]
        
        try:
            output = subprocess.run(command, capture_output=True, text=True, timeout=self.timeout + 1)
            is_alive = output.returncode == 0
            
            return {
                'ip': ip,
                'status': 'alive' if is_alive else 'dead',
                'reachable': is_alive,
                'output': output.stdout if is_alive else None
            }
        except subprocess.TimeoutExpired:
            return {'ip': ip, 'status': 'timeout', 'reachable': False}
        except Exception as e:
            return {'ip': ip, 'status': 'error', 'reachable': False, 'error': str(e)}
    
    def scan_network(self, network: str, max_workers: int = 50) -> List[Dict]:
        """
        Scan an entire network range for active hosts
        
        Args:
            network: CIDR notation network (e.g., '192.168.1.0/24')
            max_workers: Number of concurrent threads
            
        Returns:
            List of discovered hosts with their status
        """
        try:
            net = ipaddress.ip_network(network, strict=False)
            hosts = [str(ip) for ip in net.hosts()]
            
            results = []
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_ip = {executor.submit(self.ping_host, ip): ip for ip in hosts}
                
                for future in concurrent.futures.as_completed(future_to_ip):
                    result = future.result()
                    if result['reachable']:
                        results.append(result)
                        self.discovered_hosts.append(result)
            
            return results
        except ValueError as e:
            return [{'error': f'Invalid network format: {str(e)}'}]
    
    def resolve_hostname(self, ip: str) -> Optional[str]:
        """
        Resolve hostname from IP address
        
        Args:
            ip: IP address to resolve
            
        Returns:
            Hostname or None if resolution fails
        """
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            return hostname
        except socket.herror:
            return None
        except Exception:
            return None
    
    def get_mac_address(self, ip: str) -> Optional[str]:
        """
        Get MAC address for an IP (requires ARP - Windows/Linux specific)
        
        Args:
            ip: Target IP address
            
        Returns:
            MAC address or None
        """
        try:
            if platform.system().lower() == 'windows':
                output = subprocess.check_output(['arp', '-a', ip], text=True)
            else:
                output = subprocess.check_output(['arp', ip], text=True)
            
            # Parse MAC from output (basic implementation)
            for line in output.split('\n'):
                if ip in line:
                    parts = line.split()
                    for part in parts:
                        if '-' in part or ':' in part:
                            return part
            return None
        except:
            return None
    
    def discover_services(self, ip: str, common_ports: List[int] = None) -> List[Dict]:
        """
        Quick service discovery on common ports
        
        Args:
            ip: Target IP address
            common_ports: List of ports to check (default: top 20)
            
        Returns:
            List of open ports and potential services
        """
        if common_ports is None:
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 5900, 8080, 8443, 27017, 6379, 9200, 11211]
        
        open_ports = []
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:
                    service = self._identify_service(port)
                    open_ports.append({
                        'port': port,
                        'state': 'open',
                        'service': service
                    })
            except:
                pass
            finally:
                sock.close()
        
        return open_ports
    
    def _identify_service(self, port: int) -> str:
        """Map port numbers to common services"""
        service_map = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC',
            8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt', 27017: 'MongoDB',
            6379: 'Redis', 9200: 'Elasticsearch', 11211: 'Memcached'
        }
        return service_map.get(port, 'Unknown')
    
    def generate_report(self) -> Dict:
        """Generate comprehensive mapping report"""
        return {
            'total_hosts_scanned': len(self.discovered_hosts),
            'active_hosts': [h for h in self.discovered_hosts if h['reachable']],
            'summary': {
                'alive': len([h for h in self.discovered_hosts if h['reachable']]),
                'dead': len([h for h in self.discovered_hosts if not h['reachable']])
            }
        }

# CLI Interface
if __name__ == "__main__":
    mapper = AdiZenMapper()
    
    print("🗺️  AdiZen Network Mapper")
    print("=" * 50)
    
    network = input("Enter network to scan (CIDR notation, e.g., 192.168.1.0/24): ")
    
    print(f"\n[+] Scanning network: {network}")
    results = mapper.scan_network(network)
    
    print(f"\n[✓] Scan complete! Found {len(results)} active hosts:\n")
    
    for host in results:
        print(f"  → {host['ip']} - {host['status'].upper()}")
        hostname = mapper.resolve_hostname(host['ip'])
        if hostname:
            print(f"    Hostname: {hostname}")
    
    print(f"\n[+] Scan summary:")
    report = mapper.generate_report()
    print(f"    Total scanned: {report['total_hosts_scanned']}")
    print(f"    Alive: {report['summary']['alive']}")
    print(f"    Dead: {report['summary']['dead']}")


# ── Standalone wrapper function (used by Flask apps) ─────────────────────────
def map_network(network: str) -> dict:
    """
    Convenience wrapper: scan a network CIDR and return discovered hosts.

    Args:
        network: CIDR notation (e.g. '192.168.1.0/24') or single IP

    Returns:
        dict with 'network', 'active_hosts', and 'total_found'
    """
    mapper = AdiZenMapper()
    if '/' not in network:
        # Single host — just ping it
        result = mapper.ping_host(network)
        active = [result] if result.get('reachable') else []
    else:
        active = mapper.scan_network(network)

    return {
        "network": network,
        "active_hosts": active,
        "total_found": len(active)
    }
