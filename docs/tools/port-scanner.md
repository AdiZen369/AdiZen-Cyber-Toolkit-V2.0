# Port Scanner

Fast TCP port scanning for network reconnaissance and security assessment.

## Overview

The Port Scanner tool allows you to scan TCP ports on target hosts to discover open services and potential entry points. It's commonly used for:

- Network reconnaissance
- Service discovery
- Security assessments
- Attack surface analysis

## Usage

### Web Dashboard

1. Navigate to the "Port Scanner" card
2. Enter target hostname or IP address
3. Specify port range (e.g., `20-1000`)
4. Click "Start Scan"

### API Call

```bash
curl -X POST http://localhost:5000/api/scan/ports \
  -H "Content-Type: application/json" \
  -d '{"target":"scanme.nmap.org","port_range":"20-1000"}'
Python Module
python
from src.adizenports import scan_ports

result = scan_ports('scanme.nmap.org', '20-1000')
print(result)
Parameters
Parameter	Type	Required	Default	Description
target	string	Yes	-	Hostname or IP address to scan
port_range	string	No	20-1000	Port range in format START-END or single port
Response Format
json
{
  "target": "scanme.nmap.org",
  "ip": "45.33.32.156",
  "ports": "20-1000",
  "open_ports":,[1]
  "total_scanned": 981,
  "scan_time": "2026-02-15T12:00:00"
}
Common Ports
Port	Service	Description
20-21	FTP	File Transfer Protocol
22	SSH	Secure Shell
23	Telnet	Unencrypted remote access
25	SMTP	Email transmission
53	DNS	Domain Name System
80	HTTP	Web traffic
110	POP3	Email retrieval
143	IMAP	Email access
443	HTTPS	Secure web traffic
3306	MySQL	Database
3389	RDP	Remote Desktop
5432	PostgreSQL	Database
8080	HTTP-Alt	Alternative HTTP
Security Considerations
⚠️ Important:

Port scanning without authorization is illegal in many jurisdictions

Some networks have IDS/IPS that detect and block port scans

Always scan responsibly and with permission

Use rate limiting to avoid overloading targets

Ethical Scanning Checklist
✅ Written authorization obtained

✅ Scope clearly defined

✅ Time window agreed upon

✅ Notification procedures established

✅ Legal compliance verified

Tips & Best Practices
Start Small: Begin with common ports (1-1000) before scanning all 65535

Avoid Timeouts: Use reasonable timeout values for slow networks

Document Findings: Save results immediately for later analysis

Respect Rate Limits: Don't overwhelm target systems

Verify Results: Confirm open ports with additional tools

Limitations
Only scans TCP ports (UDP scanning coming in V3.0)

Does not perform service version detection

No OS fingerprinting

Sequential scanning (slower than parallel tools like nmap)

Troubleshooting
"Could not resolve hostname"
Verify the hostname is correct

Check DNS resolution: nslookup target.com

Try using IP address directly

Scan takes too long
Reduce port range

Check network connectivity

Target may have firewall blocking scans

No open ports found
Target may have firewall

Verify target is reachable: ping target.com

Try common ports only: 20-100

Related Tools
Security Auditor - Analyze web server security

Network Mapper - Map entire network topology

Header Inspector - Inspect HTTP headers

Scan responsibly. Secure ethically. 🔒