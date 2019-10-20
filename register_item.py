from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.lib
books = db.books
catalog = db.catalog


class Book:
    def __init__(self, isbn):
        check = books.find_one({'isbn': isbn})
        if check is None:
            self.isbn = isbn
            self.author = None
            self.publisher = None
            self.title = None
            self.id = self.register_book()
        else:
            self.id = check.get('_id')

    def register_book(self):
        entry = self.__dict__
        return books.insert_one(entry).inserted_id


def register_item(isbn, owner_id):
    item_id = Book(isbn).id

    item = {'item_id': item_id,
            'owner': owner_id,
            'status': 'available',
            'possession': owner_id
            }

    catalog.insert_one(item)


# Clear the db
books.drop()
catalog.drop()

isbn_test = "9788373191723"
owner_id_test = 99383
register_item(isbn_test, owner_id_test)
for book in books.find():
    pprint(book)
for item in catalog.find():
    pprint(item)
