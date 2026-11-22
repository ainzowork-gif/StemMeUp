# # Function takes html code from web page
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def take_html(url: str) -> str | None:
  headers = {"User-Agent": "Mozilla/5.0"}
  try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text
  except requests.RequestException as e:
    print(f"Request error for {url}: {e}")
    return None


# # Function to extract title
def extract_title(soup) -> str:
  if soup.title and soup.title.string:
    return soup.title.string.strip()
  return ""


# # Function to clean content and review
def extract_clean_text(soup) -> str:
  for tag in soup(["script", "style", "noscript"]):
    tag.decompose()

  raw_text = soup.get_text(separator=" ")
  return " ".join(raw_text.split())


# # Function of extract_links of pages
def extract_links(soup, base_url: str) -> list[str]:
  links = []
  for a in soup.find_all("a", href=True):
    full_link = urljoin(base_url, a["href"].strip())
    if full_link.startswith(("http://", "https://")):
      links.append(full_link)
  return links


if __name__ == "__main__":
  url = "https://example.com"  # Put url link
  headers = {"User-Agent": "Mozilla/5.0"}

  response = requests.get(url, headers=headers, timeout=10)
  soup = BeautifulSoup(response.text, "html.parser")

  print(extract_title(soup))

  clean_text = extract_clean_text(soup)
  print("Length:", len(clean_text))
  print("Sample:", clean_text[:300])

  page_links = extract_links(soup, url)
  print("Total links:", len(page_links))
  print("First 5 links:", page_links[:5])