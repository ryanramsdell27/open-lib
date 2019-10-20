from pymongo import MongoClient
from pprint import pprint
import utils
from utils import books, catalog

STATUS_AVAILABLE = "available"

class Book:
    def __init__(self, isbn):
        check = books.find_one({'isbn': isbn})
        if check is None:
            book_info = utils.get_isbn(isbn)
            
            if book_info is None:
                self.isbn = isbn
                self.author = None
                self.publisher = None
                self.title = None
                self.image = None
                self.id = self.register_book()
            else:
                self.isbn = isbn
                self.author = book_info['volumeInfo']['authors'][0]
                self.publisher = book_info['volumeInfo']['publisher']
                self.title = book_info['volumeInfo']['title']
                self.image = book_info['volumeInfo']['imageLinks']['smallThumbnail']
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

# if an item is available it is deleted from catalog
def deregister_item(item_id):
    item = catalog.find_one({'_id': item_id})
    if item.get('status') == STATUS_AVAILABLE:
        catalog.delete_one({'_id': item_id})

# Clear the db
# books.drop()
# catalog.drop()
#
# # isbn_test = "9788373191723"
# owner_id_test = 99383
# for book in books.find():
#     register_item(book.get('isbn'), owner_id_test)
# # for book in books.find():
# #     pprint(book)
# book_id = books.find_one().get('_id')
#
# for item_test in catalog.find({'owner': owner_id_test, 'item_id': book_id}):
#     pprint(item_test)
#
# deregister_item(book_id)
# print('------------------------------------')
# for item_test in catalog.find({'owner': owner_id_test, 'item_id': book_id}):
#     pprint(item_test)

