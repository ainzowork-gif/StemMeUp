# Import BeautifulSoup to parse HTML pages
from bs4 import BeautifulSoup

# Import database functions from storage.py
from sql.storage import (
    get_connection,
    create_tables,
    save_page,
    get_all_pages,
)

# Import crawler functions
from web_crawler.web_crawler import (
    crawl_website,
)

# Import preprocessing module
from indexing import preprocessing

# Import inverted index function
from indexing.inverted_index import build_inverted_index


# Function that runs the entire search engine pipeline
def run_pipeline(start_url: str, max_pages: int = 20):

    # Open a connection to the SQLite database
    conn = get_connection()

    # Create database tables if they do not already exist
    create_tables(conn)

    # Start crawling the website and collect pages
    crawled_pages = crawl_website(start_url, max_pages)

    # Loop through every page collected by the crawler
    for page_data in crawled_pages:

        # Save the page data and its links into the database
        save_page(conn, page_data)

    # Retrieve all pages stored in the database
    # This includes old pages and newly crawled pages
    all_pages = get_all_pages(conn)

    # Create an empty dictionary to store tokens for every page
    docs_tokens = {}

    # Loop through all pages retrieved from the database
    for page in all_pages:

        # Get the page ID from the database
        page_id = page["id"]

        # Get the page content
        # If content is None, use an empty string instead
        content = page["content"] or ""

        # Clean the text and convert it into tokens
        words = preprocessing.preprocess_text(content)

        # Store the tokens using the page ID as the dictionary key
        docs_tokens[page_id] = words

    # Close the database connection after retrieving all pages
    conn.close()

    # Build the inverted index using tokens from all stored pages
    # The function also saves the index into inverted.json
    index_data = build_inverted_index(docs_tokens)

    # Print the number of unique words in the inverted index
    print("Total unique words:", len(index_data))

    # Print the number of pages stored in the database
    print("Total pages in database:", len(all_pages))

    # Print the number of pages collected during this crawl
    print("Newly crawled pages:", len(crawled_pages))


# Run the pipeline only when this file is executed directly
if __name__ == "__main__":

    # Set the website URL that the crawler will start from
    start_url = [

      "https://chatgpt.com/",
      "https://docs.python.org/3/",
      "https://www.carlogos.org/car-brands/",
      "https://ar.wikihow.com/%D8%A7%D9%84%D8%B5%D9%81%D8%AD%D8%A9-%D8%A7%D9%84%D8%B1%D8%A6%D9%8A%D8%B3%D9%8A%D8%A9",
      "https://www.noor-book.com/",
    ]

    # Set the maximum number of pages to crawl
    max_pages = 5000

    # Run the complete pipeline
    run_pipeline(start_url, max_pages)