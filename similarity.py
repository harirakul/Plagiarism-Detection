"""Module for checking text."""

from difflib import SequenceMatcher

import nltk
import pandas as pd

import websearch

nltk.download("stopwords")
nltk.download("punkt")
stop_words = set(nltk.corpus.stopwords.words("english"))


def purify_text(string: str) -> str:
    """Clear text."""
    words = nltk.word_tokenize(string)
    return " ".join([word for word in words if word not in stop_words])


def web_verify(string: str, results_per_sentence: str) -> list:
    """Web verify function."""
    sentences = nltk.sent_tokenize(string)
    matching_sites = []
    for url in websearch.search(query=string, num=results_per_sentence):
        matching_sites.append(url)
    for sentence in sentences:
        for url in websearch.search(query=sentence, num=results_per_sentence):
            matching_sites.append(url)

    return list(set(matching_sites))


def similarity(str1: str, str2: str) -> float:
    """Calculate the similarity in percentages."""
    return (SequenceMatcher(None, str1, str2).ratio()) * 100


def report(text: str) -> dict:
    """Forming a report."""
    matching_sites = web_verify(purify_text(text), 2)
    matches = {}

    for i in range(len(matching_sites)):
        matches[matching_sites[i]] = similarity(
            text,
            websearch.extract_text(matching_sites[i]),
        )

    return {
        k: v for k, v in sorted(matches.items(), key=lambda item: item[1], reverse=True)
    }


def return_table(dictionary: dict) -> str:
    """Return the table."""
    search_result = pd.DataFrame({"Similarity (%)": dictionary})
    return search_result.to_html()
