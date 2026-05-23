#!/usr/bin/env python3
"""
AdiZenWorks CVE Search
Query the CIRCL CVE API and NVD for vulnerability information
Company: AdiZenWorks Inc.
"""

import json
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime


CIRCL_BASE = "https://cve.circl.lu/api"
NVD_BASE   = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def search_cve(query: str, max_results: int = 10) -> dict:
    """
    Search for CVEs by keyword or exact CVE-ID.

    Args:
        query:       CVE ID (e.g. "CVE-2021-44228") or keyword (e.g. "log4j")
        max_results: Maximum number of results to return

    Returns:
        dict with CVE entries and summary
    """
    results = {
        "query":     query,
        "scan_time": datetime.now().isoformat(),
        "source":    None,
        "cves":      [],
        "count":     0,
        "errors":    [],
    }

    query_stripped = query.strip()

    # ── EXACT CVE-ID LOOKUP ──
    if query_stripped.upper().startswith("CVE-"):
        cve_id = query_stripped.upper()
        results["mode"] = "exact"
        results["source"] = "CIRCL CVE API"

        try:
            url = f"{CIRCL_BASE}/cve/{urllib.parse.quote(cve_id)}"
            req = urllib.request.Request(
                url, headers={"User-Agent": "AdiZenWorks-CVE-Tool/2.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            if data:
                entry = _format_circl_entry(data)
                results["cves"].append(entry)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                results["errors"].append(f"CVE not found: {cve_id}")
            else:
                results["errors"].append(f"HTTP {e.code}: {e.reason}")
        except Exception as e:
            results["errors"].append(str(e))

    # ── KEYWORD SEARCH via NVD ──
    else:
        results["mode"] = "keyword"
        results["source"] = "NVD (NIST)"

        try:
            params = urllib.parse.urlencode({
                "keywordSearch": query_stripped,
                "resultsPerPage": min(max_results, 20),
                "startIndex": 0,
            })
            url = f"{NVD_BASE}?{params}"
            req = urllib.request.Request(
                url, headers={"User-Agent": "AdiZenWorks-CVE-Tool/2.0"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())

            vulns = data.get("vulnerabilities", [])
            for v in vulns[:max_results]:
                entry = _format_nvd_entry(v.get("cve", {}))
                results["cves"].append(entry)

            results["total_in_db"] = data.get("totalResults", 0)

        except urllib.error.HTTPError as e:
            results["errors"].append(f"NVD HTTP {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            results["errors"].append(f"Network error: {str(e.reason)}")
        except Exception as e:
            results["errors"].append(str(e))

    results["count"] = len(results["cves"])
    return results


def _format_circl_entry(data: dict) -> dict:
    """Normalize a CIRCL CVE entry."""
    cvss  = data.get("cvss")
    cvss3 = data.get("cvss-time") or data.get("cvssv3", {})
    return {
        "id":          data.get("id", "N/A"),
        "summary":     data.get("summary", "No description"),
        "cvss_score":  str(cvss) if cvss else "N/A",
        "cvss_v3":     str(cvss3) if cvss3 else "N/A",
        "published":   data.get("Published", "N/A"),
        "modified":    data.get("Modified", "N/A"),
        "references":  data.get("references", [])[:5],
        "cwe":         data.get("cwe", "N/A"),
        "severity":    _severity_from_score(cvss),
    }


def _format_nvd_entry(cve: dict) -> dict:
    """Normalize an NVD CVE 2.0 entry."""
    # Description
    descs = cve.get("descriptions", [])
    desc  = next((d["value"] for d in descs if d.get("lang") == "en"), "No description")

    # CVSS
    metrics    = cve.get("metrics", {})
    cvss_score = "N/A"
    cvss_v     = "N/A"
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        if key in metrics and metrics[key]:
            m = metrics[key][0]
            cvss_score = str(m.get("cvssData", {}).get("baseScore", "N/A"))
            cvss_v     = m.get("cvssData", {}).get("vectorString", "N/A")
            break

    # Refs
    refs = [r.get("url", "") for r in cve.get("references", [])[:5]]

    # CWE
    weaknesses = cve.get("weaknesses", [])
    cwe = "N/A"
    if weaknesses:
        for w in weaknesses[0].get("description", []):
            if w.get("lang") == "en":
                cwe = w.get("value", "N/A")
                break

    return {
        "id":          cve.get("id", "N/A"),
        "summary":     desc[:500],
        "cvss_score":  cvss_score,
        "cvss_v3":     cvss_v,
        "published":   cve.get("published", "N/A"),
        "modified":    cve.get("lastModified", "N/A"),
        "references":  refs,
        "cwe":         cwe,
        "severity":    _severity_from_score(cvss_score),
    }


def _severity_from_score(score) -> str:
    try:
        s = float(score)
        if s >= 9.0: return "CRITICAL"
        if s >= 7.0: return "HIGH"
        if s >= 4.0: return "MEDIUM"
        if s >= 0.1: return "LOW"
    except (TypeError, ValueError):
        pass
    return "N/A"


if __name__ == "__main__":
    r = search_cve("log4j", max_results=5)
    print(json.dumps(r, indent=2))
