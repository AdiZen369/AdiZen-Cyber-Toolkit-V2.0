// ============================================================================
// AdiZenWorks Cybersecurity Toolkit V2.0 - JavaScript
// © 2026 AdiZenWorks Inc.
// ============================================================================

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';
const SCAN_TIMEOUT = 60000; // 60 seconds

// State management
let activeScan = null;
let scanHistory = [];

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Show loading overlay
 */
function showLoading(message = 'Scanning...') {
    const overlay = document.getElementById('loading-overlay');
    const text = overlay.querySelector('.loading-text');
    if (text) text.textContent = message;
    overlay.classList.add('show');
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    overlay.classList.remove('show');
}

/**
 * Display results in a tool card
 */
function displayResults(toolId, data, isError = false) {
    const resultsDiv = document.getElementById(toolId + '-results');
    if (!resultsDiv) return;

    resultsDiv.classList.add('show');

    if (isError) {
        resultsDiv.style.color = '#FF0040';
        resultsDiv.innerHTML = `<strong>Error:</strong> ${data}`;
        return;
    }

    // Format JSON with syntax highlighting
    const formatted = JSON.stringify(data, null, 2);
    resultsDiv.style.color = '#00FF41';
    resultsDiv.innerHTML = `<pre>${escapeHtml(formatted)}</pre>`;

    // Update KPIs
    updateKPIs();
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Validate URL format
 */
function isValidUrl(string) {
    try {
        const url = new URL(string);
        return url.protocol === 'http:' || url.protocol === 'https:';
    } catch (_) {
        return false;
    }
}

/**
 * Show notification
 */
function showNotification(message, type = 'info') {
    // Simple alert for now - can be enhanced with toast notifications
    alert(message);
}

/**
 * Update KPI cards with scan statistics
 */
function updateKPIs() {
    // Count total scans from history
    const totalScans = scanHistory.length;
    document.getElementById('total-scans').textContent = totalScans;

    // Count vulnerabilities (simplified)
    let totalVulns = 0;
    scanHistory.forEach(scan => {
        if (scan.vulnerabilities) totalVulns += scan.vulnerabilities;
    });
    document.getElementById('total-vulns').textContent = totalVulns;

    // Calculate average security score
    const scores = scanHistory.filter(s => s.score).map(s => s.score);
    if (scores.length > 0) {
        const avgScore = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
        document.getElementById('security-score').textContent = avgScore + '%';
    }

    // Count critical alerts
    const critical = scanHistory.filter(s => s.risk === 'CRITICAL').length;
    document.getElementById('critical-alerts').textContent = critical;
}

// ============================================================================
// API CALL FUNCTIONS
// ============================================================================

/**
 * Generic API call handler
 */
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(API_BASE_URL + endpoint, options);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'API request failed');
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ============================================================================
// TOOL FUNCTIONS
// ============================================================================

/**
 * PORT SCANNER
 */
async function runPortScan() {
    const target = document.getElementById('port-target').value.trim();
    const portRange = document.getElementById('port-range').value.trim() || '20-1000';

    if (!target) {
        showNotification('Please enter a target hostname or IP address', 'warning');
        return;
    }

    showLoading('Scanning ports...');

    try {
        const result = await apiCall('/scan/ports', 'POST', {
            target: target,
            port_range: portRange
        });

        // Add to scan history
        scanHistory.push({
            type: 'port_scan',
            target: target,
            timestamp: new Date().toISOString(),
            vulnerabilities: result.open_ports ? result.open_ports.length : 0
        });

        displayResults('port', result);
    } catch (error) {
        displayResults('port', error.message, true);
    } finally {
        hideLoading();
    }
}

/**
 * SECURITY AUDITOR
 */
async function runSecurityAudit() {
    const url = document.getElementById('audit-url').value.trim();

    if (!url) {
        showNotification('Please enter a URL to audit', 'warning');
        return;
    }

    if (!isValidUrl(url)) {
        showNotification('Please enter a valid URL (including http:// or https://)', 'warning');
        return;
    }

    showLoading('Auditing security headers...');

    try {
        const result = await apiCall('/scan/security', 'POST', {
            url: url
        });

        // Add to scan history
        scanHistory.push({
            type: 'security_audit',
            target: url,
            timestamp: new Date().toISOString(),
            score: result.score || 0
        });

        displayResults('audit', result);
    } catch (error) {
        displayResults('audit', error.message, true);
    } finally {
        hideLoading();
    }
}

/**
 * XSS SCANNER
 */
async function runXSSScan() {
    const url = document.getElementById('xss-url').value.trim();

    if (!url) {
        showNotification('Please enter a URL to test for XSS', 'warning');
        return;
    }

    if (!isValidUrl(url)) {
        showNotification('Please enter a valid URL with a parameter (e.g., ?search=test)', 'warning');
        return;
    }

    showLoading('Testing for XSS vulnerabilities...');

    try {
        const result = await apiCall('/scan/xss', 'POST', {
            url: url
        });

        // Add to scan history
        scanHistory.push({
            type: 'xss_scan',
            target: url,
            timestamp: new Date().toISOString(),
            vulnerabilities: result.vulnerable ? 1 : 0,
            risk: result.vulnerable ? 'HIGH' : 'LOW'
        });

        displayResults('xss', result);
    } catch (error) {
        displayResults('xss', error.message, true);
    } finally {
        hideLoading();
    }
}

/**
 * SQL INJECTION TESTER
 */
async function runSQLiTest() {
    const url = document.getElementById('sqli-url').value.trim();

    if (!url) {
        showNotification('Please enter a URL to test for SQL injection', 'warning');
        return;
    }

    if (!isValidUrl(url)) {
        showNotification('Please enter a valid URL with a parameter (e.g., ?id=1)', 'warning');
        return;
    }

    showLoading('Testing for SQL injection vulnerabilities...');

    try {
        const result = await apiCall('/scan/sqli', 'POST', {
            url: url
        });

        // Add to scan history
        scanHistory.push({
            type: 'sqli_test',
            target: url,
            timestamp: new Date().toISOString(),
            vulnerabilities: result.vulnerable ? 1 : 0,
            risk: result.vulnerable ? 'CRITICAL' : 'LOW'
        });

        displayResults('sqli', result);
    } catch (error) {
        displayResults('sqli', error.message, true);
    } finally {
        hideLoading();
    }
}

/**
 * WEB SPIDER
 */
async function runWebSpider() {
    const url = document.getElementById('spider-url').value.trim();
    const maxPages = parseInt(document.getElementById('spider-pages').value) || 10;

    if (!url) {
        showNotification('Please enter a starting URL', 'warning');
        return;
    }

    if (!isValidUrl(url)) {
        showNotification('Please enter a valid URL', 'warning');
        return;
    }

    showLoading('Crawling website...');

    try {
        const result = await apiCall('/scan/spider', 'POST', {
            url: url,
            max_pages: maxPages
        });

        // Add to scan history
        scanHistory.push({
            type: 'web_spider',
            target: url,
            timestamp: new Date().toISOString(),
            pages: result.total_pages || 0
        });

        displayResults('spider', result);
    } catch (error) {
        displayResults('spider', error.message, true);
    } finally {
        hideLoading();
    }
}

/**
 * NETWORK MAPPER
 */
async function runNetworkMapper() {
    const cidr = document.getElementById('mapper-cidr').value.trim();

    if (!cidr) {
        showNotification('Please enter a network CIDR (e.g., 192.168.1.0/24)', 'warning');
        return;
    }

    // Basic CIDR validation
    if (!/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,2}$/.test(cidr)) {
        showNotification('Please enter a valid CIDR notation (e.g., 192.168.1.0/24)', 'warning');
        return;
    }

    showLoading('Mapping network... This may take a few minutes.');

    try {
        const result = await apiCall('/scan/network', 'POST', {
            network: cidr
        });

        // Add to scan history
        scanHistory.push({
            type: 'network_map',
            target: cidr,
            timestamp: new Date().toISOString(),
            devices: result.hosts_found || 0
        });

        displayResults('mapper', result);
    } catch (error) {
        displayResults('mapper', error.message, true);
    } finally {
        hideLoading();
    }
}

/**
 * HASH GENERATOR
 */
async function runHashGenerator() {
    const text = document.getElementById('hash-text').value.trim();
    const algorithm = document.getElementById('hash-algorithm').value;

    if (!text) {
        showNotification('Please enter text to hash', 'warning');
        return;
    }

    showLoading('Generating hash...');

    try {
        const result = await apiCall('/tool/hash', 'POST', {
            text: text,
            algorithm: algorithm
        });

        displayResults('hash', result);
    } catch (error) {
        displayResults('hash', error.message, true);
    } finally {
        hideLoading();
    }
}

/**
 * HEADER INSPECTOR
 */
async function runHeaderInspector() {
    const url = document.getElementById('header-url').value.trim();

    if (!url) {
        showNotification('Please enter a URL to inspect', 'warning');
        return;
    }

    if (!isValidUrl(url)) {
        showNotification('Please enter a valid URL', 'warning');
        return;
    }

    showLoading('Inspecting headers...');

    try {
        const result = await apiCall('/tool/headers', 'POST', {
            url: url
        });

        displayResults('header', result);
    } catch (error) {
        displayResults('header', error.message, true);
    } finally {
        hideLoading();
    }
}

/**
 * AI ASSISTANT
 */
async function askAI() {
    const question = document.getElementById('ai-question').value.trim();

    if (!question) {
        showNotification('Please enter a question', 'warning');
        return;
    }

    showLoading('Consulting AI assistant...');

    try {
        const result = await apiCall('/ai/ask', 'POST', {
            question: question
        });

        const resultsDiv = document.getElementById('ai-results');
        resultsDiv.classList.add('show');

        if (result.error) {
            resultsDiv.style.color = '#FFD700';
            resultsDiv.innerHTML = `<strong>Note:</strong> ${result.error}`;
        } else {
            resultsDiv.style.color = '#FFFFFF';
            resultsDiv.innerHTML = `<strong>AI Response:</strong><br><br>${escapeHtml(result.answer)}`;
        }
    } catch (error) {
        const resultsDiv = document.getElementById('ai-results');
        resultsDiv.classList.add('show');
        resultsDiv.style.color = '#FF0040';
        resultsDiv.innerHTML = `<strong>Error:</strong> ${error.message}`;
    } finally {
        hideLoading();
    }
}

// ============================================================================
// EVENT LISTENERS & INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', function () {
    console.log('AdiZenWorks Cybersecurity Toolkit V2.0 - Initialized');

    // Add Enter key support for inputs
    const inputs = document.querySelectorAll('.input');
    inputs.forEach(input => {
        input.addEventListener('keypress', function (e) {
            if (e.key === 'Enter' && input.tagName !== 'TEXTAREA') {
                // Find the button in the same tool-form
                const form = input.closest('.tool-form, .ai-form');
                if (form) {
                    const button = form.querySelector('.btn');
                    if (button) button.click();
                }
            }
        });
    });

    // Initialize KPIs
    updateKPIs();

    // Add smooth scroll for nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }

                // Update active state
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });

    // Add fade-in animation to tool cards
    const toolCards = document.querySelectorAll('.tool-card');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, { threshold: 0.1 });

    toolCards.forEach(card => observer.observe(card));
});

// ============================================================================
// KEYBOARD SHORTCUTS
// ============================================================================

document.addEventListener('keydown', function (e) {
    // Ctrl+K or Cmd+K to focus AI input
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('ai-question').focus();
    }

    // Escape to close loading overlay (emergency stop)
    if (e.key === 'Escape') {
        hideLoading();
    }
});

// ============================================================================
// EXPORT FUNCTIONS (Make available globally)
// ============================================================================

window.runPortScan = runPortScan;
window.runSecurityAudit = runSecurityAudit;
window.runXSSScan = runXSSScan;
window.runSQLiTest = runSQLiTest;
window.runWebSpider = runWebSpider;
window.runNetworkMapper = runNetworkMapper;
window.runHashGenerator = runHashGenerator;
window.runHeaderInspector = runHeaderInspector;
window.askAI = askAI;