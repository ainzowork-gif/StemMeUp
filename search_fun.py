import json
from indexing import preprocessing

# access to inverted index
with open("indexing/inverted.json", "r", encoding="utf-8") as file:
    inverted_index = json.load(file)


def search_query(query, index):

    # apply preprocessing on query
    terms = preprocessing.preprocess_text(query)

    results = []

    # search the index for each word
    for term in terms:

        # access page ids for the word
        pages = index.get(term, [])

        # add page ids to results
        for page_id in pages:
            if page_id not in results:
                results.append(page_id)

    return results


# search
