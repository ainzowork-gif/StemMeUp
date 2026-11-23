from collections import deque
import time
from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup
import requests


# Function takes html code from web page
def take_html(url: str) -> str | None:
  headers = {"User-Agent": "Mozilla/5.0"}
  try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text
  except requests.RequestException as e:
    print(f"Request error for {url}: {e}")
    return None


# Function to extract title
def extract_title(soup: BeautifulSoup) -> str:
      #see the title and make sure that he have contant (Ahmed)
  if soup.title and soup.title.string:
    return soup.title.string.strip()
  return ""


# Function to clean content and review
def extract_clean_text(soup: BeautifulSoup) -> str:
  for tag in soup(["script", "style", "noscript"]):
    tag.decompose()

  raw_text = soup.get_text(separator=" ")
  return " ".join(raw_text.split())


# Function to extract links from page
def extract_links(soup: BeautifulSoup, base_url: str) -> list[str]:
  links = []
  #the loop check if the a syntax have a real url
  for a in soup.find_all("a", href=True):
    full_link = urljoin(base_url, a["href"].strip())
    clean_link, _ = urldefrag(full_link)
    if clean_link.startswith(("http://", "https://")):
      links.append(clean_link)
  return list(dict.fromkeys(links))


# Check if URL belongs to the same domain
def is_same_domain(url: str, base_url: str) -> bool:
  return urlparse(url).netloc.lower() == urlparse(base_url).netloc.lower()


# Crawl website starting from start_url
def crawl_website(start_urls: list[str], max_pages: int = 20) -> list[dict]:
    
    # Make sure start_urls is a list
    if isinstance(start_urls, str):
        start_urls = [start_urls]

    # Remove fragments and duplicate URLs
    clean_start_urls = []

    for url in start_urls:
        clean_url, _ = urldefrag(url)

        if clean_url not in clean_start_urls:
            clean_start_urls.append(clean_url)

    # Add all starting URLs to the queue
    url_queue = deque(clean_start_urls)

    # Track visited URLs
    visited = set()

    # Store successfully crawled pages
    crawled_pages = []

    while url_queue and len(crawled_pages) < max_pages:

        current_url = url_queue.popleft()

        if current_url in visited:
            continue

        visited.add(current_url)

        print("Crawling:", current_url)

        html = take_html(current_url)

        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")

        title = extract_title(soup)
        content = extract_clean_text(soup)
        links = extract_links(soup, current_url)

        page_data = {
            "url": current_url,
            "title": title,
            "content": content,
            "links": links,
        }

        crawled_pages.append(page_data)

        # Add links from the current page
        for link in links:

            if (
                link not in visited
                and link not in url_queue
            ):
                url_queue.append(link)

        time.sleep(1)

    print("\nCrawling finished")
    print("Visited pages:", len(visited))
    print("Successfully collected pages:", len(crawled_pages))
    print("URLs still waiting:", len(url_queue))
    return crawled_pages

if __name__ == "__main__":
  start_url =[]
  max_pages = 100

  pages = crawl_website(start_url, max_pages)

  print("\nTotal pages:", len(pages))
  for page in pages:
    print("\nTitle:", page["title"])
    print("URL:", page["url"])
    print("Content length:", len(page["content"]))