from bs4 import BeautifulSoup
from sql.storage import get_connection, create_tables, save_page
from web_crawler.web_crawler import (
    take_html,
    extract_title,
    extract_clean_text,
    extract_links,
)
from indexing import preprocessing
from indexing.inverted_index import build_inverted_index


def run_pipeline(urls: list[str]):

    # so we connect to database
    conn = get_connection()

    # so we create database tables
    create_tables(conn)

    # dictionary to store words of all pages
    docs_tokens = {}

    # loop on all urls
    for url in urls:

        # so we can extract the html and read it
        html = take_html(url)

        if not html:
            print("there is something wrong")
            continue

        # convert html to beautiful soup
        soup = BeautifulSoup(html, "html.parser")

        # extract page data
        title = extract_title(soup)
        content = extract_clean_text(soup)
        links = extract_links(soup, url)

        # so save our data in dic
        page_data = {
            "url": url,
            "title": title,
            "content": content,
            "links": links
        }

        # save page in database
        page_id = save_page(conn, page_data)

        # apply preprocessing on page content
        words = preprocessing.preprocess_text(content)

        # store words with page id
        docs_tokens[page_id] = words

    # close database connection
    conn.close()

    # build inverted index
    index_data = build_inverted_index(docs_tokens)

    print("Total indexed words:", len(index_data))


if __name__ == "__main__":

    # urls that we want to crawl

    target_urls = [
    "https://en.wikipedia.org/wiki/Machine_learning",
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://en.wikipedia.org/wiki/Data_science",
    "https://en.wikipedia.org/wiki/Information_retrieval",
    "https://en.wikipedia.org/wiki/Search_engine",
    "https://en.wikipedia.org/wiki/Lionel_Messi",
    "https://www.wikihow.com/Tell-a-Story",
    "https://en.wikipedia.org/wiki/Cristiano_Ronaldo"
]


    # run the pipeline
    run_pipeline(target_urls)