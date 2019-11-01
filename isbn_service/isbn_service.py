import re

from database.database import DatabaseDriver
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

        # Check cache
        book = self.database_driver.lookup(isbn)

        # Check 3rd party if non-existent
        if book is None:
            try:
                # Check primary source
                book = self.google_books.lookup(isbn)
            except ISBNNotFound:
                try:
                    # Check secondary source
                    book = self.open_library.lookup(isbn)
                except ISBNNotFound:
                    return None

            # Update cache
            self.database_driver.insert(book)

        return book
