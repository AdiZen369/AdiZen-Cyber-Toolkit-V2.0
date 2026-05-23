#!/usr/bin/env python3
"""
AdiZenWorks DNS Lookup
Multi-record DNS resolver for reconnaissance
Company: AdiZenWorks Inc.
"""

import socket
from datetime import datetime

# Try dnspython for advanced lookups
try:
    import dns.resolver
    import dns.reversename
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False


def dns_lookup(domain: str) -> dict:
    """
    Perform comprehensive DNS lookup on a domain.

    Returns:
        dict with A, AAAA, MX, NS, TXT, CNAME records and reverse PTR
    """
    results = {
        "domain": domain,
        "scan_time": datetime.now().isoformat(),
        "records": {},
        "errors": [],
    }

    if DNS_AVAILABLE:
        record_types = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 10

        for rtype in record_types:
            try:
                answers = resolver.resolve(domain, rtype)
                results["records"][rtype] = [str(r) for r in answers]
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NXDOMAIN:
                results["errors"].append(f"Domain does not exist: {domain}")
                break
            except dns.resolver.Timeout:
                results["errors"].append(f"Timeout resolving {rtype} for {domain}")
            except Exception as e:
                results["errors"].append(f"{rtype}: {str(e)}")

        # Reverse PTR for first A record
        if "A" in results["records"] and results["records"]["A"]:
            ip = results["records"]["A"][0]
            try:
                rev = dns.reversename.from_address(ip)
                ptr = resolver.resolve(rev, "PTR")
                results["records"]["PTR"] = [str(r) for r in ptr]
            except Exception:
                pass

    else:
        # Fallback: basic socket resolution
        try:
            ip = socket.gethostbyname(domain)
            results["records"]["A"] = [ip]
        except socket.gaierror as e:
            results["errors"].append(str(e))

        # Reverse lookup
        if "A" in results["records"] and results["records"]["A"]:
            try:
                hostname = socket.gethostbyaddr(results["records"]["A"][0])[0]
                results["records"]["PTR"] = [hostname]
            except Exception:
                pass

        results["note"] = "Install dnspython for full MX/NS/TXT support: pip install dnspython"

    total = sum(len(v) for v in results["records"].values())
    results["total_records"] = total
    return results


if __name__ == "__main__":
    import json
    r = dns_lookup("google.com")
    print(json.dumps(r, indent=2))
