import re

from database.database import DatabaseDriver
from .exceptions import InvalidISBN, ISBNNotFound
from .google_books_api import GoogleBooksAPI
from .book import Book


def format_isbn(isbn: str):
    return re.sub('[^0-9]', '', isbn)


def validate_isbn(isbn: str):
    if len(isbn) != 13 and len(isbn) != 10:
        raise InvalidISBN

    # if not re.match('[^0-9]', isbn):
    #     raise InvalidISBN


class ISBNService:

    def __init__(self, google_books_api_key: str):
        self.database_driver = DatabaseDriver()
        self.google_books = GoogleBooksAPI(google_books_api_key)

    def lookup(self, isbn: str) -> Book:
        isbn = format_isbn(isbn)

        validate_isbn(isbn)

        # Check cache
        book = self.database_driver.lookup(isbn)

        # Check 3rd party if non-existent
        if book is None:
            # TODO: Check secondary source
            try:
                book = self.google_books.lookup(isbn)
            except ISBNNotFound:
                return None
            # TODO: Check ...

            self.database_driver.insert(book)

        return book
