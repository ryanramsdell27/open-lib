from datetime import datetime
from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.lib
books = db.books
catalog = db.catalog
users = db.users
events = db.events

DEFAULT_LOAN_PERIOD = 21

STATUS_IN_PROCESS = 'in_process'
STATUS_AVAILABLE = "available"

EVENT_REQUEST = 'request'
EVENT_CANCEL = 'cancel'
EVENT_TRANSACTION = 'transaction'


class Event:
    def __init__(self, request_type, item_id, owner_id, borrower_id):
        self.request_type = request_type
        self.item_id = item_id
        self.owner = owner_id
        self.borrower = borrower_id
        self.event_date = datetime.timestamp(datetime.now())


# Start a request for a loan
def event_request(borrower_id, item_id, loan_period=DEFAULT_LOAN_PERIOD):
    # TODO check that the book is available

    # create new event
    owner_id = catalog.find_one({'item_id': item_id}).get('owner')
    event = Event(EVENT_REQUEST, item_id, owner_id, borrower_id)
    event.due_date = event.event_date + loan_period
    # add event to db
    events.insert_one(event.__dict__)
    # change status of item in catalog
    catalog.update_one({'item_id': item_id}, {'$set': {'status': STATUS_IN_PROCESS}})

    # TODO notify owner of request


# Cancel a fulfillment request
def event_cancel(borrower_id, item_id):
    # create a new event
    owner_id = catalog.find_one({'item_id': item_id}).get('owner')
    event = Event(EVENT_CANCEL, item_id, owner_id, borrower_id)
    # add event to db
    events.insert_one(event.__dict__)
    # change status of item in catalog
    catalog.update_one({'item_id': item_id}, {'$set': {'status': STATUS_AVAILABLE}})

    # TODO notify borrower of cancel


test_user = users.find_one()
test_item = catalog.find_one()
event_request(test_user.get('_id'), test_item.get('item_id'))
event_cancel(test_user.get('_id'), test_item.get('item_id'))
for event in events.find():
    pprint(event)
