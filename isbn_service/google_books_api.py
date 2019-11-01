import requests
from .book import Book
from .exceptions import ISBNNotFound


class GoogleBooksAPI:
    def __init__(self, api_key):
        self.endpoint = 'https://www.googleapis.com/books/v1/volumes'
        self.api_key = api_key

    def lookup(self, isbn: str) -> Book:
        params = {
            'q': isbn,
            'key': self.api_key
        }

        r = requests.get(self.endpoint, params=params)

        if r.status_code != 200:
            raise ISBNNotFound

        if r.json()["kind"] != "books#volumes":
            raise ISBNNotFound

        if r.json()["totalItems"] == 0:
            raise ISBNNotFound

        volume_info = r.json()["items"][0].get("volumeInfo", {})
        image_links = volume_info.get("imageLinks", {})

        return Book(
            isbn=isbn,
            title=volume_info.get("title", ""),
            subtitle=volume_info.get("subtitle", ""),
            authors=volume_info.get("authors", []),
            publisher=volume_info.get("publisher", ""),
            publisher_date=volume_info.get("publisherDate", ""),
            description=volume_info.get("description", ""),
            page_count=volume_info.get("pageCount", ""),
            image_links=[i for i in image_links.values()]
        )
