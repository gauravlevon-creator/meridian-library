"""
Lightweight local "Ask the Librarian" search model.

This is a small TF-IDF + cosine-similarity model trained on the catalogue's
own title/author/genre/description text, so natural-language queries like
"something about how computers talk to each other" can still surface
"Computer Networks" even without an exact keyword match. It runs entirely
locally with no external API calls or API key.

Swapping in a hosted LLM later (e.g. the Anthropic API) is a drop-in
replacement: keep the same `search(query, top_k)` signature in this file,
and call the model instead of the vectorizer below. The rest of the app
(the /api/assistant/search endpoint and the frontend) would not need to change.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class LibraryAssistant:
    def __init__(self):
        self._vectorizer = None
        self._matrix = None
        self._books = []

    def fit(self, books):
        """books: list of sqlite3.Row or dict with title/author/genre/description/etc."""
        self._books = list(books)
        corpus = [
            f"{b['title']} {b['author']} {b['genre']} {b['description']}"
            for b in self._books
        ]
        self._vectorizer = TfidfVectorizer(stop_words="english")
        self._matrix = self._vectorizer.fit_transform(corpus)

    def search(self, query: str, top_k: int = 5):
        if not query or self._vectorizer is None or not self._books:
            return []

        query_vec = self._vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self._matrix).flatten()

        ranked = sorted(
            zip(self._books, scores), key=lambda pair: pair[1], reverse=True
        )

        results = []
        for book, score in ranked[:top_k]:
            if score <= 0:
                continue
            item = dict(book)
            item["match_score"] = round(float(score), 3)
            results.append(item)
        return results


assistant = LibraryAssistant()
