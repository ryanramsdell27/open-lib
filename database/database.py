from pymongo import MongoClient
from isbn_service.book import Book


class DatabaseDriver:

    def __init__(self, username: str, password: str):
        self.client = MongoClient("mongodb+srv://" +
                                  username +
                                  ":" +
                                  password +
                                  "@cluster0-1ftoj.mongodb.net/test?retryWrites=true&w=majority")
        self.db = self.client.lib
        self.books = self.db.books
        self.catalog = self.db.catalog
        self.users = self.db.users
        self.events = self.db.events
        self.pending_transactions = self.db.pending_transactions

    def lookup(self, isbn: str) -> Book:
        book = self.books.find_one(
            {
                'isbn': isbn
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
