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

def get_catalog_item(isbn, owner_id):
    return catalog.find_one({'item_id': get_book(isbn)['_id'], 'owner': owner_id})

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

def get_pending_codes(code_owner):
    pt =  pending_transactions.find({'code_owner': code_owner})
    output = []
    for transaction in pt:
        book_id = events.find_one({'_id': transaction.get('event_token')}).get('item_id')
        if (transaction.get('code_owner') != transaction.get('code_recipient')):
            output.append(
                {
                    'event_token': transaction.get('event_token'),
                    'verification_code': transaction.get('verification_code'),
                    'code_owner': transaction.get('code_owner'),
                    'code_recipient': transaction.get('code_recipient'),
                    'code_owner_name': users.find_one({'_id': transaction.get('code_owner')}).get('name'),
                    'code_recipient_name': users.find_one({'_id': transaction.get('code_recipient')}).get('name'),
                    'code_owner_email': users.find_one({'_id': transaction.get('code_owner')}).get('email'),
                    'code_recipient_email': users.find_one({'_id': transaction.get('code_recipient')}).get('email'),
                    'item_title': books.find_one({'_id': book_id}).get('title')
                }
            )
    pprint.pprint(output)
    return output

def get_pending_verifications(code_recipient):
    pt =  pending_transactions.find({'code_recipient': code_recipient})
    output = []
    for transaction in pt:
        book_id = events.find_one({'_id': transaction.get('event_token')}).get('item_id')
        if (transaction.get('code_owner') != transaction.get('code_recipient')):
            output.append(
                {
                    'event_token': transaction.get('event_token'),
                    'verification_code': transaction.get('verification_code'),
                    'code_owner': transaction.get('code_owner'),
                    'code_recipient': transaction.get('code_recipient'),
                    'code_owner_name': users.find_one({'_id': transaction.get('code_owner')}).get('name'),
                    'code_recipient_name': users.find_one({'_id': transaction.get('code_recipient')}).get('name'),
                    'code_owner_email': users.find_one({'_id': transaction.get('code_owner')}).get('email'),
                    'code_recipient_email': users.find_one({'_id': transaction.get('code_recipient')}).get('email'),
                    'item_title': books.find_one({'_id': book_id}).get('title')
                }
            )
    pprint.pprint(output)
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

def get_pending_transaction(code_recipient):
    return pending_transactions.find_one({'code_recipient': code_recipient})

def get_isbn(isbn: str) -> dict:
    payload = {
        'q': 'isbn:' + isbn
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params=payload)

    if r.status_code != 200 or 'items' not in r.json():
        return None

    info = r.json()['items'][0]

    return info