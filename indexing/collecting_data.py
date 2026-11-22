import json
import requests
import time

# Wikipedia API URL
url = "https://en.wikipedia.org/w/api.php"

# Request headers
headers = {
    "User-Agent": "SearchEngineIndexer/1.0 (your-real-email@example.com)"
}

# Read articles from JSON file
with open("articles.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

# Loop through all articles
for article in articles:

    # Get page ID
    page_id = article["page_id"]

    # Request article content
    params = {
        "action": "query",
        "pageids": page_id,
        "prop": "extracts",
        "explaintext": True,
        "format": "json"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        # Access article content
        page = data["query"]["pages"][str(page_id)]
        content = page.get("extract", "")

        # Update article content
        article["content"] = content

        print(f"Downloaded: {article['title']}")

    except Exception as error:
        print(f"Error with {article['title']}: {error}")

    # Wait before next request
    time.sleep(1)

# Save updated articles
with open("articles.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, ensure_ascii=False, indent=4)
