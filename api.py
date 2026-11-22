from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from search_fun import search_query, inverted_index
from sql.storage import get_connection, get_page


app = FastAPI()

# allow the frontend to connect to the api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# receive the search query
class SearchRequest(BaseModel):
    query: str


@app.post("/search")
def search(request: SearchRequest):

    query = request.query.strip()

    if not query:
        return {"results": []}

    # search for page ids
    page_ids = search_query(query, inverted_index)

    # connect to database
    conn = get_connection()

    results = []

    # get page information
    for page_id in page_ids:

        page = get_page(conn, int(page_id))

        if page:
            results.append({
                "title": page["title"],
                "url": page["url"],
                "content": page["content"]
            })

    conn.close()

    return {"results": results}