import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def crawl_url(url):
    """
    Crawls a single URL and extracts technical SEO data.
    Returns a dictionary containing metrics and found elements.
    """
    
    # 1. Input Validation
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    results = {
        "url": url,
        "status_code": 0,
        "load_time": 0,
        "title": "Missing",
        "meta_desc": "Missing",
        "h1": [],
        "h2": [],
        "images": [],  # List of dicts: {'src': ..., 'alt': ...}
        "internal_links": 0,
        "external_links": 0,
        "error": None
    }

    try:
        # 2. Performance Check (TTFB / Load Time)
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SmartSpider/1.0; +http://your-portfolio.com)'
        }
        
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        end_time = time.time()
        
        results["load_time"] = round(end_time - start_time, 4)
        results["status_code"] = response.status_code

        # 3. If request is successful, parse HTML
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract Title
            if soup.title and soup.title.string:
                results["title"] = soup.title.string.strip()
            
            # Extract Meta Description
            meta = soup.find('meta', attrs={'name': 'description'})
            if meta and meta.get('content'):
                results["meta_desc"] = meta['content'].strip()

            # Extract Headers
            results["h1"] = [h.get_text(strip=True) for h in soup.find_all('h1')]
            results["h2"] = [h.get_text(strip=True) for h in soup.find_all('h2')]

            # Extract Images (Src & Alt)
            imgs = soup.find_all('img')
            for img in imgs:
                src = img.get('src')
                alt = img.get('alt', '').strip()
                if src:
                    # Handle relative URLs
                    full_src = urljoin(url, src)
                    results["images"].append({"src": full_src, "alt": alt})

            # Count Links
            links = soup.find_all('a', href=True)
            domain = urlparse(url).netloc
            for link in links:
                href = link['href']
                if domain in href or href.startswith('/'):
                    results["internal_links"] += 1
                else:
                    results["external_links"] += 1

    except requests.exceptions.RequestException as e:
        results["error"] = f"Connection Error: {str(e)}"
    
    return results