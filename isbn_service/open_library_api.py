import requests
from .book import Book
from .exceptions import ISBNNotFound


class OpenLibraryAPI:
    def __init__(self):
        self.endpoint = 'https://openlibrary.org/api/books'

    def lookup(self, isbn: str) -> Book:
        params = {
            "bibkeys": "ISBN:" + isbn,
            "format": "json",
            "jscmd": "details"
        }

        r = requests.get(self.endpoint, params=params)

        if r.status_code != 200:
            raise ISBNNotFound

        book = r.json().get("ISBN:" + isbn)
        if book is None:
            raise ISBNNotFound

        details = book.get("details")
        if details is None:
            raise ISBNNotFound

        publishers = details.get("publishers", [""])
        authors = details.get("authors", [])

        return Book(
            isbn=isbn,
            title=details.get("title", ""),
            subtitle=details.get("subtitle", ""),
            authors=[author.get("name") for author in authors],
            publisher=publishers[0],
            publisher_date=details.get("publish_date", ""),
            description=details.get("description", ""),
            page_count=details.get("number_of_pages", ""),
            image_links=[book.get("thumbnail_url")]
        )
