#!/usr/bin/env python3
"""
AdiZenWorks Subdomain Enumerator
DNS-based subdomain brute-forcing and enumeration
Company: AdiZenWorks Inc.
"""

import socket
import concurrent.futures
from datetime import datetime
from typing import List, Dict


# Built-in wordlist — 80 common subdomains
DEFAULT_WORDLIST = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "ns2",
    "ns3", "ns4", "cpanel", "whm", "autodiscover", "autoconfig", "m", "mobile",
    "imap", "test", "api", "dev", "dev2", "staging", "beta", "portal", "secure",
    "vpn", "remote", "admin", "manage", "dashboard", "ops", "monitor", "status",
    "blog", "news", "shop", "store", "cdn", "media", "images", "img", "static",
    "assets", "upload", "uploads", "files", "download", "downloads", "app",
    "apps", "login", "auth", "oauth", "sso", "id", "account", "accounts",
    "support", "help", "docs", "documentation", "wiki", "kb", "community",
    "forum", "git", "gitlab", "github", "jira", "confluence", "jenkins",
    "ci", "build", "deploy", "k8s", "kubernetes", "docker", "grafana",
    "prometheus", "elastic", "kibana", "db", "database", "mysql", "redis",
    "mongo", "postgres", "backup", "old", "v1", "v2", "staging2", "uat",
]


def enumerate_subdomains(
    domain: str,
    wordlist: List[str] = None,
    max_workers: int = 30,
    timeout: float = 2.0,
) -> Dict:
    """
    Brute-force enumerate subdomains via DNS resolution.

    Args:
        domain:      Base domain to scan (e.g. "example.com")
        wordlist:    List of subdomain prefixes to test
        max_workers: Thread pool size (default 30)
        timeout:     DNS timeout per query in seconds

    Returns:
        dict with found subdomains and summary stats
    """
    words   = wordlist or DEFAULT_WORDLIST
    results = {
        "domain":       domain,
        "scan_time":    datetime.now().isoformat(),
        "tested":       len(words),
        "found":        [],
        "not_found":    0,
        "errors":       [],
    }

    def check(sub: str) -> Dict | None:
        fqdn = f"{sub}.{domain}"
        try:
            socket.setdefaulttimeout(timeout)
            ip = socket.gethostbyname(fqdn)
            return {"subdomain": fqdn, "ip": ip}
        except socket.gaierror:
            return None
        except Exception as e:
            return {"subdomain": fqdn, "error": str(e)}

    not_found_count = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(check, w): w for w in words}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res is None:
                not_found_count += 1
            elif "error" in res:
                not_found_count += 1
            else:
                results["found"].append(res)

    results["not_found"]   = not_found_count
    results["found_count"] = len(results["found"])
    # Sort alphabetically
    results["found"].sort(key=lambda x: x["subdomain"])
    return results


if __name__ == "__main__":
    import json
    r = enumerate_subdomains("example.com", max_workers=20)
    print(json.dumps(r, indent=2))
