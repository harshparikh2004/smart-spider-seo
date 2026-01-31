import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def crawl_url(url):
    """
    Crawls the URL and extracts technical SEO data + Internal Links for the Graph.
    """
    start_time = time.time()
    
    try:
        # Spoof a real browser to avoid getting blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Basic SEO Metrics
        title = soup.title.string.strip() if soup.title else "Missing"
        meta_desc = "Missing"
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get('content', 'Missing')
            
        # 2. Extract Images
        images = []
        img_tags = soup.find_all('img')
        for img in img_tags:
            src = img.get('src')
            if src:
                # Convert relative paths (/assets/img.png) to absolute (https://site.com/assets/img.png)
                full_src = urljoin(url, src)
                alt = img.get('alt', '')
                images.append({'src': full_src, 'alt': alt})

        # 3. Extract Internal Links (NEW FOR GRAPH)
        internal_links = set() # Use a set to avoid duplicates
        base_domain = urlparse(url).netloc
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            # Join relative URLs
            full_link = urljoin(url, href)
            parsed_link = urlparse(full_link)
            
            # Check if it's internal (same domain) and not a fragment (#)
            if parsed_link.netloc == base_domain and parsed_link.scheme in ['http', 'https']:
                # Clean up trailing slashes for consistency
                clean_link = full_link.rstrip('/')
                if clean_link != url.rstrip('/'): # Don't link to self
                    internal_links.add(clean_link)

        load_time = round(time.time() - start_time, 2)
        
        return {
            "status_code": response.status_code,
            "load_time": load_time,
            "title": title,
            "meta_desc": meta_desc,
            "images": images,
            "internal_links_count": len(internal_links),
            "found_links": list(internal_links)[:30] # Limit to 30 for the graph (prevents lag)
        }

    except Exception as e:
        return {"error": str(e)}