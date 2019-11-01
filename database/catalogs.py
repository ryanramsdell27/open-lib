from pymongo.collection import Collection
from isbn_service.book import Book


class BooksCatalog:
    books: Collection

    def __init__(self, books: Collection):
        self.books = books

    def isbn_lookup(self, isbn: str) -> Book:
        book = self.books.find_one(
            {
                "isbn": isbn
            }
        )

        if book is not None:
            return Book(
                oid=book.get("_id", ""),
                isbn=isbn,
                title=book.get("title", ""),
                subtitle=book.get("subtitle", ""),
                authors=book.get("authors", []),
                publisher=book.get("publisher", ""),
                publisher_date=book.get("publisher_date", ""),
                description=book.get("description", ""),
                page_count=book.get("page_count", ""),
                image_links=book.get("image_links", [])
            )
        return book

    def insert(self, book: Book):
        self.books.insert_one(book.__dict__)


class CatalogCatalog:
    catalog: Collection

    def __init__(self, catalog: Collection):
        self.catalog = catalog


class EventsCatalog:
    events: Collection

    def __init__(self, events: Collection):
        self.events = events


class UsersCatalog:
    users: Collection

    def __init__(self, users: Collection):
        self.users = users


class PendingTransactionsCatalog:
    pending_transactions: Collection

    def __init__(self, pending_transactions: Collection):
        self.pending_transactions = pending_transactions
