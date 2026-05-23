// AdiZen Cybersecurity Toolkit - Frontend JavaScript
// API endpoints match web/app.py routes

// --- Utility ---
function showResult(elementId, data) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
}

function showLoading(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) el.innerHTML = '<p class="loading">⏳ ' + message + '</p>';
}

// --- Port Scanner ---
async function runPortScan() {
    const target = document.getElementById('port-target')?.value?.trim();
    const ports = document.getElementById('port-range')?.value?.trim() || '20-1000';

    if (!target) { alert('Please enter a target'); return; }

    showLoading('port-results', 'Scanning ports...');

    try {
        const response = await fetch('/api/port-scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target, ports })
        });
        const data = await response.json();
        showResult('port-results', data);
    } catch (error) {
        showResult('port-results', { error: error.message });
    }
}

// --- Security Audit (Headers) ---
async function runSecurityAudit() {
    const url = document.getElementById('audit-url')?.value?.trim();
    if (!url) { alert('Please enter a URL'); return; }

    showLoading('audit-results', 'Auditing headers...');

    try {
        const response = await fetch('/api/check-headers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await response.json();
        showResult('audit-results', data);
    } catch (error) {
        showResult('audit-results', { error: error.message });
    }
}

// --- XSS Scanner ---
async function runXSSScan() {
    const url = document.getElementById('xss-url')?.value?.trim();
    if (!url) { alert('Please enter a URL'); return; }

    showLoading('xss-results', 'Scanning for XSS...');

    try {
        const response = await fetch('/api/xss-scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await response.json();
        showResult('xss-results', data);
    } catch (error) {
        showResult('xss-results', { error: error.message });
    }
}

// --- SQL Injection Scanner ---
async function runSQLiScan() {
    const url = document.getElementById('sqli-url')?.value?.trim();
    if (!url) { alert('Please enter a URL'); return; }

    showLoading('sqli-results', 'Scanning for SQL injection...');

    try {
        const response = await fetch('/api/sqli-scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await response.json();
        showResult('sqli-results', data);
    } catch (error) {
        showResult('sqli-results', { error: error.message });
    }
}

// --- Network Mapper ---
async function runNetworkMap() {
    const target = document.getElementById('network-target')?.value?.trim();
    if (!target) { alert('Please enter a network (e.g. 192.168.1.0/24)'); return; }

    showLoading('network-results', 'Mapping network...');

    try {
        const response = await fetch('/api/network-map', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target })
        });
        const data = await response.json();
        showResult('network-results', data);
    } catch (error) {
        showResult('network-results', { error: error.message });
    }
}

// --- Web Spider ---
async function runWebSpider() {
    const url = document.getElementById('spider-url')?.value?.trim();
    const depth = parseInt(document.getElementById('spider-depth')?.value || '2');
    if (!url) { alert('Please enter a URL'); return; }

    showLoading('spider-results', 'Crawling website...');

    try {
        const response = await fetch('/api/web-spider', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, depth })
        });
        const data = await response.json();
        showResult('spider-results', data);
    } catch (error) {
        showResult('spider-results', { error: error.message });
    }
}

// --- Hash Generator ---
async function runHashGenerate() {
    const text = document.getElementById('hash-text')?.value?.trim();
    const algorithm = document.getElementById('hash-algo')?.value || 'sha256';
    if (!text) { alert('Please enter text to hash'); return; }

    try {
        const response = await fetch('/api/generate-hash', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, algorithm })
        });
        const data = await response.json();
        showResult('hash-results', data);
    } catch (error) {
        showResult('hash-results', { error: error.message });
    }
}

// --- DNS Lookup ---
async function runDNSLookup() {
    const domain = document.getElementById('dns-domain')?.value?.trim();
    if (!domain) { alert('Please enter a domain'); return; }

    showLoading('dns-results', 'Looking up DNS records...');

    try {
        const response = await fetch('/api/dns-lookup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ domain })
        });
        const data = await response.json();
        showResult('dns-results', data);
    } catch (error) {
        showResult('dns-results', { error: error.message });
    }
}

// --- SSL Inspector ---
async function runSSLInspect() {
    const hostname = document.getElementById('ssl-hostname')?.value?.trim();
    const port = parseInt(document.getElementById('ssl-port')?.value || '443');
    if (!hostname) { alert('Please enter a hostname'); return; }

    showLoading('ssl-results', 'Inspecting SSL/TLS...');

    try {
        const response = await fetch('/api/ssl-inspect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ hostname, port })
        });
        const data = await response.json();
        showResult('ssl-results', data);
    } catch (error) {
        showResult('ssl-results', { error: error.message });
    }
}

// --- Password Strength ---
async function runPasswordCheck() {
    const password = document.getElementById('password-input')?.value?.trim();
    if (!password) { alert('Please enter a password'); return; }

    showLoading('password-results', 'Analyzing password strength...');

    try {
        const response = await fetch('/api/password-check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password })
        });
        const data = await response.json();
        showResult('password-results', data);
    } catch (error) {
        showResult('password-results', { error: error.message });
    }
}

// --- Subdomain Enumerator ---
async function runSubdomainEnum() {
    const domain = document.getElementById('subdomain-domain')?.value?.trim();
    if (!domain) { alert('Please enter a domain'); return; }

    showLoading('subdomain-results', 'Enumerating subdomains...');

    try {
        const response = await fetch('/api/subdomain-enum', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ domain })
        });
        const data = await response.json();
        showResult('subdomain-results', data);
    } catch (error) {
        showResult('subdomain-results', { error: error.message });
    }
}

// --- CVE Search ---
async function runCVESearch() {
    const query = document.getElementById('cve-query')?.value?.trim();
    const maxResults = parseInt(document.getElementById('cve-max')?.value || '10');
    if (!query) { alert('Please enter a search query'); return; }

    showLoading('cve-results', 'Searching CVE databases...');

    try {
        const response = await fetch('/api/cve-search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, max_results: maxResults })
        });
        const data = await response.json();
        showResult('cve-results', data);
    } catch (error) {
        showResult('cve-results', { error: error.message });
    }
}

// --- Reverse Shell Detector ---
async function runRevShellDetect() {
    const text = document.getElementById('revshell-text')?.value?.trim();
    if (!text) { alert('Please enter code or text to scan'); return; }

    showLoading('revshell-results', 'Scanning for reverse shells...');

    try {
        const response = await fetch('/api/revshell-detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        showResult('revshell-results', data);
    } catch (error) {
        showResult('revshell-results', { error: error.message });
    }
}

// --- Security Audit (Full) ---
async function runFullSecurityAudit() {
    const url = document.getElementById('secaudit-url')?.value?.trim();
    if (!url) { alert('Please enter a URL'); return; }

    showLoading('secaudit-results', 'Running full security audit...');

    try {
        const response = await fetch('/api/security-audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const data = await response.json();
        showResult('secaudit-results', data);
    } catch (error) {
        showResult('secaudit-results', { error: error.message });
    }
}

// --- AI Assistant ---
async function runAIAssistant() {
    const question = document.getElementById('ai-question')?.value?.trim();
    if (!question) { alert('Please enter a question'); return; }

    showLoading('ai-results', 'Consulting AI...');

    try {
        const response = await fetch('/api/ai-assistant', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        const data = await response.json();
        showResult('ai-results', data);
    } catch (error) {
        showResult('ai-results', { error: error.message });
    }
}
