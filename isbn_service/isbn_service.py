import os
import re

from .exceptions import InvalidISBN, ISBNNotFound
from .google_books_api import GoogleBooksAPI


def format_isbn(isbn: str):
    return re.sub('[^0-9]', '', isbn)


def validate_isbn(isbn: str):
    if len(isbn) != 13 and len(isbn) != 10:
        raise InvalidISBN

    if not re.match('[^0-9]', isbn):
        raise InvalidISBN

    pass


class ISBNService:

    def __init__(self):
        self.gba = GoogleBooksAPI(os.environ["GOOGLE_BOOKS_API_KEY"])

    def lookup(self, isbn: str):
        isbn = format_isbn(isbn)

        validate_isbn(isbn)

        # TODO: Check cache

        try:
            book = self.gba.lookup(isbn)
        except ISBNNotFound:
            book = None

        # TODO: Check secondary source
        # TODO: Check ...

        return book
