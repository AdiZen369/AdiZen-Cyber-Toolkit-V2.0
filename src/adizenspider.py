"""
AdiZen Web Spider - Automated Web Crawler for Endpoint Discovery
Author: AdiZenWorks Inc.
License: MIT
"""

import requests
import urllib3
from bs4 import BeautifulSoup

# Suppress InsecureRequestWarning when verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import urljoin, urlparse
from typing import Set, List, Dict, Optional
import time
import re

class AdiZenSpider:
    """Web crawler for discovering URLs, forms, and endpoints"""
    
    def __init__(self, base_url: str, max_depth: int = 3, delay: float = 0.5):
        self.base_url = base_url
        self.max_depth = max_depth
        self.delay = delay
        self.visited_urls = set()
        self.discovered_urls = set()
        self.forms = []
        self.subdomains = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AdiZen-Spider/2.0 (Security Scanner)'
        })
    
    def crawl(self, url: Optional[str] = None, depth: int = 0) -> Dict:
        """
        Recursively crawl website starting from base_url
        
        Args:
            url: Starting URL (defaults to base_url)
            depth: Current recursion depth
            
        Returns:
            Dictionary with crawl results
        """
        if url is None:
            url = self.base_url
        
        if depth > self.max_depth or url in self.visited_urls:
            return {'status': 'skipped', 'reason': 'depth_limit or already_visited'}
        
        self.visited_urls.add(url)
        
        try:
            response = self.session.get(url, timeout=10, verify=False, allow_redirects=True)
            response.raise_for_status()
            
            # Parse page content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract all links
            links = self._extract_links(soup, url)
            
            # Extract forms
            forms = self._extract_forms(soup, url)
            self.forms.extend(forms)
            
            # Extract subdomains
            subdomains = self._extract_subdomains(soup, url)
            self.subdomains.update(subdomains)
            
            # Extract API endpoints
            api_endpoints = self._extract_api_endpoints(soup, response.text)
            
            # Recursively crawl discovered links
            for link in links:
                if self._is_same_domain(link, self.base_url):
                    time.sleep(self.delay)  # Rate limiting
                    self.crawl(link, depth + 1)
            
            return {
                'url': url,
                'status_code': response.status_code,
                'links_found': len(links),
                'forms_found': len(forms),
                'depth': depth
            }
        
        except requests.exceptions.RequestException as e:
            return {'url': url, 'status': 'error', 'error': str(e)}
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """Extract all hyperlinks from page"""
        links = set()
        
        for tag in soup.find_all(['a', 'link'], href=True):
            href = tag.get('href')
            full_url = urljoin(base_url, href)
            
            # Filter out non-HTTP protocols
            if urlparse(full_url).scheme in ['http', 'https']:
                links.add(full_url)
                self.discovered_urls.add(full_url)
        
        return links
    
    def _extract_forms(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extract all forms and their inputs"""
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                'url': url,
                'action': urljoin(url, form.get('action', '')),
                'method': form.get('method', 'get').upper(),
                'inputs': []
            }
            
            for input_tag in form.find_all('input'):
                form_data['inputs'].append({
                    'name': input_tag.get('name'),
                    'type': input_tag.get('type', 'text'),
                    'value': input_tag.get('value', '')
                })
            
            for textarea in form.find_all('textarea'):
                form_data['inputs'].append({
                    'name': textarea.get('name'),
                    'type': 'textarea',
                    'value': textarea.text
                })
            
            forms.append(form_data)
        
        return forms
    
    def _extract_subdomains(self, soup: BeautifulSoup, base_url: str) -> Set[str]:
        """Extract potential subdomains from links"""
        subdomains = set()
        base_domain = urlparse(base_url).netloc
        
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            full_url = urljoin(base_url, href)
            domain = urlparse(full_url).netloc
            
            if domain != base_domain and base_domain in domain:
                subdomains.add(domain)
        
        return subdomains
    
    def _extract_api_endpoints(self, soup: BeautifulSoup, html_content: str) -> Set[str]:
        """Extract potential API endpoints from scripts"""
        endpoints = set()
        
        # Look for common API patterns in scripts
        api_patterns = [
            r'/api/[a-zA-Z0-9/_-]+',
            r'/v\d+/[a-zA-Z0-9/_-]+',
            r'\.json',
            r'/rest/[a-zA-Z0-9/_-]+'
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, html_content)
            endpoints.update(matches)
        
        return endpoints
    
    def _is_same_domain(self, url1: str, url2: str) -> bool:
        """Check if two URLs belong to same domain"""
        return urlparse(url1).netloc == urlparse(url2).netloc
    
    def find_sensitive_files(self) -> List[str]:
        """Search for common sensitive files"""
        sensitive_files = [
            'robots.txt', 'sitemap.xml', '.git/config', '.env',
            'config.php', 'wp-config.php', 'web.config',
            'composer.json', 'package.json', '.htaccess'
        ]
        
        found_files = []
        base_parsed = urlparse(self.base_url)
        base = f"{base_parsed.scheme}://{base_parsed.netloc}"
        
        for file in sensitive_files:
            url = urljoin(base, file)
            try:
                response = self.session.head(url, timeout=5)
                if response.status_code == 200:
                    found_files.append(url)
            except:
                pass
        
        return found_files
    
    def generate_report(self) -> Dict:
        """Generate comprehensive crawl report"""
        return {
            'base_url': self.base_url,
            'total_urls_discovered': len(self.discovered_urls),
            'total_urls_visited': len(self.visited_urls),
            'forms_discovered': len(self.forms),
            'subdomains_discovered': list(self.subdomains),
            'all_urls': list(self.discovered_urls),
            'forms': self.forms,
            'sensitive_files': self.find_sensitive_files()
        }

# CLI Interface
if __name__ == "__main__":
    print("🕷️  AdiZen Web Spider")
    print("=" * 50)
    
    target = input("Enter target URL (e.g., https://example.com): ")
    max_depth = int(input("Enter max crawl depth (1-5): ") or "2")
    
    spider = AdiZenSpider(target, max_depth=max_depth)
    
    print(f"\n[+] Starting crawl of {target}")
    print(f"[+] Max depth: {max_depth}\n")
    
    spider.crawl()
    
    report = spider.generate_report()
    
    print(f"\n[✓] Crawl complete!")
    print(f"    URLs discovered: {report['total_urls_discovered']}")
    print(f"    URLs visited: {report['total_urls_visited']}")
    print(f"    Forms found: {report['forms_discovered']}")
    print(f"    Subdomains found: {len(report['subdomains_discovered'])}")
    print(f"    Sensitive files: {len(report['sensitive_files'])}")
    
    if report['sensitive_files']:
        print(f"\n[!] Sensitive files discovered:")
        for file in report['sensitive_files']:
            print(f"    → {file}")


# ── Standalone wrapper function (used by Flask apps) ─────────────────────────
def spider_website(url: str, max_depth: int = 2) -> dict:
    """
    Convenience wrapper: crawl a website and return a report dict.

    Args:
        url: Base URL to crawl
        max_depth: Maximum recursion depth (default 2)

    Returns:
        Crawl report dict
    """
    spider = AdiZenSpider(url, max_depth=max_depth)
    spider.crawl()
    return spider.generate_report()


# Alias for backward compatibility with root app.py
def crawl_website(url: str, max_pages: int = 10) -> dict:
    """Alias for spider_website with max_pages mapped to max_depth."""
    return spider_website(url, max_depth=min(max_pages, 5))
