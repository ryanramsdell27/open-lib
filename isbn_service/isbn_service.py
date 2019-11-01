import re

from database.database_driver import DatabaseDriver
from .exceptions import InvalidISBN, ISBNNotFound
from .google_books_api import GoogleBooksAPI
from .open_library_api import OpenLibraryAPI
from .book import Book
from environment import GOOGLE_BOOKS_API_KEY, MONGODB_USERNAME, MONGODB_PASSWORD


def format_isbn(isbn: str):
    return re.sub('[^0-9]', '', isbn)


def validate_isbn(isbn: str):
    if len(isbn) != 13 and len(isbn) != 10:
        raise InvalidISBN


class ISBNService:

    def __init__(self):
        self.database_driver = DatabaseDriver(MONGODB_USERNAME, MONGODB_PASSWORD)
        self.google_books = GoogleBooksAPI(GOOGLE_BOOKS_API_KEY)
        self.open_library = OpenLibraryAPI()

    def lookup(self, isbn: str) -> Book:
        isbn = format_isbn(isbn)
        validate_isbn(isbn)

        # ISBN information sources by priority - cache should always be checked first
        isbn_sources = [self.google_books, self.open_library]

        # Check cache
        book = self.database_driver.lookup(isbn)

        if book is not None:
            # Cache hit
            return book
        else:
            # Cache miss - lookup on each source and exit on first success
            for isbn_source in isbn_sources:
                try:
                    book = isbn_source.lookup(isbn)

                    # Update cache
                    self.database_driver.insert(book)
                    break
                except ISBNNotFound:
                    book = None

        return book
