#!/usr/bin/env python3
"""
AdiZenWorks Password Strength Analyzer
Entropy-based password scoring with NIST-aligned recommendations
Company: AdiZenWorks Inc.
"""

import math
import string
from datetime import datetime


# Common weak passwords (top-100 subset)
COMMON_PASSWORDS = {
    "password", "123456", "password1", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon", "baseball",
    "iloveyou", "master", "sunshine", "ashley", "bailey", "passw0rd",
    "shadow", "123123", "654321", "superman", "qazwsx", "michael",
    "football", "password123", "admin", "welcome", "1q2w3e4r", "admin123",
}


def analyze_password(password: str) -> dict:
    """
    Analyze password strength using entropy, complexity, and pattern checks.

    Returns:
        dict with score, grade, entropy, issues, and recommendations
    """
    results = {
        "password_length": len(password),
        "masked":          "●" * len(password),
        "scan_time":       datetime.now().isoformat(),
    }

    if not password:
        results.update({"score": 0, "grade": "F", "issues": ["Empty password"]})
        return results

    # ── CHARACTER POOL SIZE ──
    pool = 0
    has_lower   = any(c in string.ascii_lowercase for c in password)
    has_upper   = any(c in string.ascii_uppercase for c in password)
    has_digit   = any(c in string.digits for c in password)
    has_special = any(c in string.punctuation for c in password)

    if has_lower:   pool += 26
    if has_upper:   pool += 26
    if has_digit:   pool += 10
    if has_special: pool += 32

    results["character_classes"] = {
        "lowercase":  has_lower,
        "uppercase":  has_upper,
        "digits":     has_digit,
        "special":    has_special,
        "pool_size":  pool,
    }

    # ── ENTROPY ──
    entropy = len(password) * math.log2(pool) if pool > 0 else 0
    results["entropy_bits"] = round(entropy, 2)

    # ── PATTERN CHECKS ──
    issues = []
    recs   = []

    if password.lower() in COMMON_PASSWORDS:
        issues.append("Password is in the common password list")
        recs.append("Choose a unique passphrase — avoid dictionary words")

    if len(password) < 8:
        issues.append("Too short (< 8 characters)")
        recs.append("Use at least 12 characters")
    elif len(password) < 12:
        recs.append("Increase to 16+ characters for maximum security")

    if not has_upper:
        issues.append("No uppercase letters")
        recs.append("Add uppercase letters (A-Z)")
    if not has_digit:
        issues.append("No digits")
        recs.append("Add numbers (0-9)")
    if not has_special:
        issues.append("No special characters")
        recs.append("Add special characters (!@#$%^&*...)")

    # Sequential patterns
    seq_chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    pw_lower  = password.lower()
    for i in range(len(pw_lower) - 2):
        chunk = pw_lower[i:i+3]
        if chunk in seq_chars or chunk[::-1] in seq_chars:
            issues.append("Contains sequential pattern (e.g. abc, 123)")
            recs.append("Avoid sequential characters")
            break

    # Repeated characters
    if len(set(password)) < len(password) * 0.5:
        issues.append("Many repeated characters")
        recs.append("Use more unique characters")

    # ── SCORING ──
    score = 0
    score += min(30, len(password) * 2)          # length: up to 30
    score += 10 if has_lower   else 0
    score += 10 if has_upper   else 0
    score += 10 if has_digit   else 0
    score += 15 if has_special else 0
    score += min(25, int(entropy / 4))            # entropy bonus: up to 25
    score -= len(issues) * 8                      # deduct for issues
    score  = max(0, min(100, score))

    # ── GRADE ──
    if score >= 85:
        grade, label = "A", "Very Strong"
    elif score >= 70:
        grade, label = "B", "Strong"
    elif score >= 50:
        grade, label = "C", "Moderate"
    elif score >= 30:
        grade, label = "D", "Weak"
    else:
        grade, label = "F", "Very Weak"

    results.update({
        "score":           score,
        "grade":           grade,
        "strength":        label,
        "issues":          issues,
        "recommendations": recs,
        "crack_estimate":  _crack_time(entropy),
    })

    return results


def _crack_time(entropy: float) -> str:
    """Estimate offline brute-force crack time at 10B guesses/sec."""
    if entropy <= 0:
        return "Instant"
    combinations = 2 ** entropy
    guesses_per_sec = 10_000_000_000  # 10 billion (GPU cracking)
    seconds = combinations / guesses_per_sec

    if seconds < 1:
        return "Instant"
    elif seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    elif seconds < 31536000 * 1000:
        return f"{seconds/31536000:.1f} years"
    else:
        return "Centuries+"


if __name__ == "__main__":
    import json
    r = analyze_password("P@ssw0rd!")
    print(json.dumps(r, indent=2))
