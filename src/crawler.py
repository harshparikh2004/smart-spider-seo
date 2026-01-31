import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random

def get_random_header():
    # Rotates headers to avoid detection
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }

def crawl_url(url):
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
        "images": [],
        "internal_links": 0,
        "external_links": 0,
        "error": None
    }

    try:
        start_time = time.time()
        # Use headers and a generous timeout
        response = requests.get(url, headers=get_random_header(), timeout=10)
        end_time = time.time()
        
        results["load_time"] = round(end_time - start_time, 2)
        results["status_code"] = response.status_code

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if soup.title: results["title"] = soup.title.string.strip()
            
            meta = soup.find('meta', attrs={'name': 'description'})
            if meta: results["meta_desc"] = meta.get('content', 'Missing').strip()

            results["h1"] = [h.get_text(strip=True) for h in soup.find_all('h1')]
            results["h2"] = [h.get_text(strip=True) for h in soup.find_all('h2')][:5]

            # Get Images
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    results["images"].append({
                        "src": urljoin(url, src),
                        "alt": img.get('alt', '').strip()
                    })

            # Count Links
            for link in soup.find_all('a', href=True):
                if urlparse(url).netloc in link['href']:
                    results["internal_links"] += 1
                else:
                    results["external_links"] += 1
        else:
            results["error"] = f"Status {response.status_code}"

    except Exception as e:
        results["error"] = str(e)
    
    return results