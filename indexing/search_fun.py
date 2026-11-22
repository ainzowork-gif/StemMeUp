import json

#acssec to inverted index
with open("indexing/inverted.json", "r", encoding="utf-8") as file:
    inverted_index = json.load(file)

def search_query(query, index):
    results = []

    #we split it ti words
    terms = query.lower().split()

    #searh the index for the world
    for term in terms:

        # acsses page id for the word
        pages = index.get(term, [])

        # add page id for the ressult
        for page_id in pages:
            if page_id not in results:
                results.append(page_id)

    return results


#search
query = input("Enter your search query: ")

results = search_query(query, inverted_index)

print(results)