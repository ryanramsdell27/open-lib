from pymongo import MongoClient
from .catalogs import *


class DatabaseDriver:

    def __init__(self, username: str, password: str):
        self.client = MongoClient("mongodb+srv://" +
                                  username +
                                  ":" +
                                  password +
                                  "@cluster0-1ftoj.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client.lib
        self.books_catalog = BooksCatalog(self.db.books)
        self.catalog_catalog = CatalogCatalog(self.db.catalog)
        self.users_catalog = UsersCatalog(self.db.users)
        self.events_catalog = EventsCatalog(self.db.events)
        self.pending_transactions_catalog = PendingTransactionsCatalog(self.db.pending_transactions)

    def lookup(self, isbn: str) -> Book:
        return self.books_catalog.isbn_lookup(isbn)

    def insert(self, book: Book):
        self.books_catalog.insert(book)
