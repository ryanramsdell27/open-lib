from pymongo import MongoClient
import register_item, register_user
from utils import books, catalog

def populate_db():
    isbns = [
        '0060977582',
        '9780385490818',
        '9780553447453',
        '9780316005043',
        '9780007488308',
        '9780345339683',
        '9781985086593',
        '9780521795401', #topology
        '9780984782857'
    ]

    for isbn in isbns:
        register_item.register_item(isbn, register_user.get_user_id('payton.r.g@gmail.com'))

populate_db()