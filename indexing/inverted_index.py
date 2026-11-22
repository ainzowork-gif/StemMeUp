import json

# we build the inverted index
def build_inverted_index(docs_tokens, output_path="indexing/inverted.json"):

    inverted_index = {}

    # loop on all pages and words
    for page_id, words in docs_tokens.items():
        for word in words:

            if word not in inverted_index:
                # so we add the word like the key
                inverted_index[word] = []

            # we add the id so it will be the value
            if page_id not in inverted_index[word]:
                inverted_index[word].append(page_id)

    # we build json file for the inverted index
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(inverted_index, file, ensure_ascii=False, indent=4)

    return inverted_index