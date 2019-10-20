from pymongo import MongoClient
import requests
import pprint

client = MongoClient()
db = client.lib
books = db.books
catalog = db.catalog
users = db.users
events = db.events
pending_transactions = db.pending_transactions

def get_book(isbn):
    return books.find_one({'isbn': isbn})

def get_catalog_items():
    items = catalog.find({})
    output = []
    for item in items:
        if item['status'] == 'available':
            book = books.find_one({'_id': item['item_id']})
            owner = users.find_one({'_id': item['owner']})
            possession = users.find_one({'_id': item['possession']})
            output.append(
                {
                    'isbn': book['isbn'],
                    'title': book['title'],
                    'publisher': book['publisher'],
                    'author': book['author'],
                    'image': book['image'],
                    'owner': owner['email'],
                    'possession': possession['name'],
                    'status': item['status']
                }
            )
    return output

def get_user_items(id):
    items = catalog.find({'owner': id})
    output = []
    for item in items:
        book = books.find_one({'_id': item['item_id']})
        owner = users.find_one({'_id': item['owner']})
        possession = users.find_one({'_id': item['possession']})
        output.append(
            {
                'isbn': book['isbn'],
                'title': book['title'],
                'publisher': book['publisher'],
                'author': book['author'],
                'image': book['image'],
                'owner': owner['name'],
                'possession': possession['name'],
                'status': item['status']
            }
        )
        
    return output

def get_isbn(isbn: str) -> dict:
    payload = {
        'q': 'isbn:' + isbn
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params=payload)

    if r.status_code != 200 or 'items' not in r.json():
        return None

    info = r.json()['items'][0]

    return info