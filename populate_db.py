from pymongo import MongoClient
import register_item

client = MongoClient()
db = client.lib
books = db.books
catalog = db.catalog

def populate_db():
    isbns = [
        '0060977582',
        '9780385490818',
        '9780553447453',
        '9780316005043',
        '9780007488308',
        '9780345339683'
    ]

    for isbn in isbns:
        register_item.register_item(isbn, 1)