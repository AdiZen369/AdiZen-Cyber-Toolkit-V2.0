#!/usr/bin/env python3
"""
AdiZenWorks SSL/TLS Inspector
Certificate validation, expiry, and cipher analysis
Company: AdiZenWorks Inc.
"""

import ssl
import socket
import json
from datetime import datetime, timezone


def inspect_ssl(hostname: str, port: int = 443) -> dict:
    """
    Inspect SSL/TLS certificate and connection details for a hostname.

    Returns:
        dict with cert info, validity, expiry, protocols, and security rating
    """
    results = {
        "hostname": hostname,
        "port": port,
        "scan_time": datetime.now().isoformat(),
        "status": "unknown",
        "errors": [],
    }

    # ── CERTIFICATE RETRIEVAL ──
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                protocol = ssock.version()

        # Subject / Issuer
        def _parse_rdns(rdns):
            return {k: v for entry in rdns for k, v in entry}

        subject = _parse_rdns(cert.get("subject", []))
        issuer  = _parse_rdns(cert.get("issuer", []))

        results["certificate"] = {
            "subject":        subject,
            "issuer":         issuer,
            "common_name":    subject.get("commonName", "N/A"),
            "org":            subject.get("organizationName", "N/A"),
            "issuer_org":     issuer.get("organizationName", "N/A"),
            "serial_number":  cert.get("serialNumber", "N/A"),
            "version":        cert.get("version", "N/A"),
        }

        # SANs
        san_list = []
        for san_type, san_value in cert.get("subjectAltName", []):
            san_list.append(f"{san_type}: {san_value}")
        results["certificate"]["san"] = san_list

        # Validity dates
        fmt = "%b %d %H:%M:%S %Y %Z"
        not_before_str = cert.get("notBefore", "")
        not_after_str  = cert.get("notAfter", "")

        try:
            not_before = datetime.strptime(not_before_str, fmt).replace(tzinfo=timezone.utc)
            not_after  = datetime.strptime(not_after_str, fmt).replace(tzinfo=timezone.utc)
            now        = datetime.now(timezone.utc)
            days_left  = (not_after - now).days

            results["validity"] = {
                "not_before":   not_before_str,
                "not_after":    not_after_str,
                "days_remaining": days_left,
                "is_valid":     not_before <= now <= not_after,
                "is_expired":   now > not_after,
            }

            if days_left <= 0:
                results["status"] = "EXPIRED"
            elif days_left <= 14:
                results["status"] = "CRITICAL — expires soon"
            elif days_left <= 30:
                results["status"] = "WARNING — expires soon"
            else:
                results["status"] = "VALID"
        except Exception as e:
            results["validity"] = {"error": str(e)}

        # Cipher / Protocol
        results["tls"] = {
            "protocol":        protocol,
            "cipher_suite":    cipher[0] if cipher else "N/A",
            "cipher_bits":     cipher[2] if cipher else "N/A",
        }

        # Security flags
        flags = []
        if cipher and cipher[2] and cipher[2] < 128:
            flags.append("WEAK_CIPHER_BITS")
        if protocol in ("TLSv1", "TLSv1.1", "SSLv2", "SSLv3"):
            flags.append("DEPRECATED_PROTOCOL")
        results["security_flags"] = flags

        # Overall rating
        if results.get("validity", {}).get("is_expired"):
            results["rating"] = "F — Certificate Expired"
        elif "DEPRECATED_PROTOCOL" in flags or "WEAK_CIPHER_BITS" in flags:
            results["rating"] = "C — Weak TLS Config"
        elif results["status"] == "VALID":
            results["rating"] = "A — Good"
        else:
            results["rating"] = "B"

    except ssl.SSLCertVerificationError as e:
        results["status"] = "INVALID — Verification Failed"
        results["errors"].append(str(e))
        results["rating"] = "F — Cert Verification Error"
    except ssl.SSLError as e:
        results["status"] = "SSL Error"
        results["errors"].append(str(e))
    except socket.timeout:
        results["status"] = "Timeout"
        results["errors"].append(f"Connection to {hostname}:{port} timed out")
    except ConnectionRefusedError:
        results["status"] = "Refused"
        results["errors"].append(f"Connection refused on {hostname}:{port}")
    except Exception as e:
        results["status"] = "Error"
        results["errors"].append(str(e))

    return results


if __name__ == "__main__":
    r = inspect_ssl("google.com")
    print(json.dumps(r, indent=2))
