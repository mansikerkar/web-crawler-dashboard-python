import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited = set()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; InternshipCrawler/1.0)"
}

def crawl(url, depth, keyword=None):
    results = []

    if depth <= 0 or url in visited:
        return results

    visited.add(url)

    try:
        response = requests.get(url, headers=HEADERS, timeout=6)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "N/A"
        text = soup.get_text(" ", strip=True)

        if not keyword or keyword.lower() in text.lower():
            results.append({
                "url": url,
                "title": title,
                "text": text[:800]
            })

        # Follow internal/external links
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])

            parsed = urlparse(next_url)
            if parsed.scheme in ["http", "https"]:
                results.extend(crawl(next_url, depth - 1, keyword))

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")

    return results

