from pymongo import MongoClient
import requests
import pprint

client = MongoClient()
db = client.lib
books = db.books
catalog = db.catalog

def get_books():
    return books.find()

def get_isbn(isbn: str) -> dict:
    payload = {
        'q': 'isbn:' + isbn
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params=payload)

    pprint.pprint(r.json())

    if r.status_code != 200 or 'items' not in r.json():
        return None

    info = r.json()['items'][0]

    return info

# isbn='0060977582'
# pprint.pprint(get_isbn(isbn))