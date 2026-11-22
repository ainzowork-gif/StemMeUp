import json
import string
from nltk.stem import PorterStemmer

with open("articles.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

    # so we access the dict in the list
    token_list = {}

    # words that we will delete because they are not important
    stop_words = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
        "below", "between", "both", "but", "by", "can", "can't", "cannot", "could",
        "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
        "during", "each", "few", "for", "from", "further", "had", "hadn't", "has",
        "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her",
        "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's",
        "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
        "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
        "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
        "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't",
        "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
        "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
        "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
        "they've", "this", "those", "through", "to", "too", "under", "until", "up",
        "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
        "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
        "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
        "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
        "yourself", "yourselves"
    }

    ps = PorterStemmer()


def preprocess_text(text):
    clean_word = []

    # Lowercasing
    l_article = (text or "").lower()

    # Punctuation Removal
    p_article = l_article.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Tokenization
    tokens = p_article.split()

    # Stop Words Removal + Stemming
    for word in tokens:
        if word not in stop_words:
            stemmed_word = ps.stem(word)
            clean_word.append(stemmed_word)

    return clean_word


# so we apply preprocessing on all articles
for article in articles:
    token_list[article["page_id"]] = preprocess_text(article["content"])

print(token_list)