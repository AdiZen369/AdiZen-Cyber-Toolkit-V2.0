# Security Policy

## Supported Versions

Currently supported versions of AdiZenWorks Cybersecurity Toolkit:

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in the toolkit itself, please report it responsibly.

### How to Report

**DO NOT create a public GitHub issue for security vulnerabilities.**

Instead, please email: **security@adizenworks.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

- **Initial Response:** Within 48 hours
- **Status Update:** Within 7 days
- **Fix Timeline:** Depends on severity
  - Critical: 1-7 days
  - High: 7-14 days
  - Medium: 14-30 days
  - Low: Next release cycle

### Disclosure Policy

- We follow coordinated disclosure
- We'll work with you to understand and fix the issue
- Public disclosure after fix is released
- Credit given to security researchers (if desired)

## Security Best Practices

### For Users

1. **Keep Updated:** Always use the latest version
2. **API Keys:** Never commit config.json to public repositories
3. **Permissions:** Run with minimum required privileges
4. **Networks:** Test only on isolated/authorized networks
5. **Backups:** Maintain backups before running scans

### For Contributors

1. **Code Review:** All PRs undergo security review
2. **Dependencies:** Keep dependencies updated
3. **Input Validation:** Validate and sanitize all inputs
4. **Error Handling:** Don't expose sensitive information in errors
5. **Secrets:** Use environment variables, never hardcode

## Known Limitations

The toolkit has inherent limitations users should be aware of:

1. **No Authentication:** Local web dashboard has no auth (by design)
2. **HTTP Only:** AI features transmit data over HTTPS to Google
3. **Local Storage:** Scan results stored locally in plain JSON
4. **Network Exposure:** Port scanning may trigger IDS/IPS
5. **Rate Limiting:** No built-in rate limiting (V2.0)

## Security Features

### Current (V2.0)

- ✅ Input validation on all tools
- ✅ XSS prevention in web interface
- ✅ Secure API key storage (gitignored)
- ✅ No remote code execution vectors
- ✅ Error messages don't leak sensitive data

### Planned (V3.0)

- 🔄 User authentication for web dashboard
- 🔄 Encrypted report storage
- 🔄 Rate limiting and throttling
- 🔄 Audit logging
- 🔄 RBAC (Role-Based Access Control)

## Compliance

This toolkit is designed for:
- ✅ Penetration testing (with authorization)
- ✅ Security research
- ✅ Educational purposes
- ✅ Internal security assessments

Not designed for:
- ❌ Compliance auditing (PCI-DSS, HIPAA, etc.)
- ❌ Production security monitoring
- ❌ Automated security operations

## Third-Party Dependencies

We use the following third-party libraries:
- Flask (BSD-3-Clause)
- Requests (Apache 2.0)
- BeautifulSoup4 (MIT)
- Google Generative AI (Apache 2.0)

All dependencies are regularly updated and scanned for vulnerabilities.

## Questions?

For general security questions (not vulnerabilities):
- Email: security@adizenworks.com
- GitHub Discussions: [Link to discussions]

---

**Security is a journey, not a destination. Stay vigilant. 🔒**