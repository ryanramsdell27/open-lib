from datetime import datetime
from pymongo import MongoClient
from pprint import pprint
from utils import books, catalog, users, events, pending_transactions
import random

DEFAULT_LOAN_PERIOD = 21

STATUS_IN_PROCESS = 'in_process'
STATUS_AVAILABLE = "available"
STATUS_ON_LOAN = "on_loan"

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


class Transaction:
    def __init__(self, event_token, verification_code, code_owner, code_recipient):
        self.event_token = event_token
        self.verification_code = verification_code
        self.code_owner = code_owner
        self.code_recipient = code_recipient


# Start a request for a loan
def event_request(borrower_id, item_id, loan_period=DEFAULT_LOAN_PERIOD):
    # TODO check that the book is available

    # create new event
    owner_id = catalog.find_one({'item_id': item_id}).get('owner')
    event = Event(EVENT_REQUEST, item_id, owner_id, borrower_id)
    event.due_date = event.event_date + loan_period
    # add event to db
    event_id = events.insert_one(event.__dict__).inserted_id
    # change status of item in catalog
    catalog.update_one({'item_id': item_id}, {'$set': {'status': STATUS_IN_PROCESS}})

    # TODO notify owner of request
    trans = Transaction(event_id, random.randint(1000, 9999), borrower_id, owner_id)
    pending_transactions.insert_one(trans.__dict__)
    return event_id


def event_transaction(verify_token):
    verify_event = events.find_one({'_id': verify_token})
    item_id = verify_event.get('item_id')
    item = catalog.find_one({'item_id': item_id})

    last_event = events.find({'item_id': item_id}).sort('event_date', -1).next()

    borrower_id = last_event.get('borrower')
    owner_id = last_event.get('owner')

    if last_event.get('_id') != verify_token:
        print('Verification failed, item status has changed')
        pending_transactions.delete_one({'event_token': verify_token})
        return None

    event_type = last_event.get('request_type')

    # Physical p2p book loaned out, owner enters borrower code
    event_id = None
    if event_type == EVENT_REQUEST:
        # create event
        event = Event(EVENT_TRANSACTION, item_id, borrower_id, owner_id)
        # add event to db
        event_id = events.insert_one(event.__dict__).inserted_id
        # Change book possession to user
        catalog.update_one({'item_id': item_id}, {'$set': {'status': STATUS_ON_LOAN, 'possession': borrower_id}})

        trans = Transaction(event_id, random.randint(1000, 9999), owner_id, borrower_id)
        trans.zdumb = "SHITTTTT"
        pending_transactions.insert_one(trans.__dict__)

    elif event_type == EVENT_CANCEL:
        print('Error: an item should not be verified after cancellation')

    elif event_type == EVENT_TRANSACTION:
        # Return item
        if item.get('status') == STATUS_ON_LOAN:
            # create event
            event = Event(EVENT_TRANSACTION, item_id, borrower_id, owner_id)
            # add event to db
            event_id = events.insert_one(event.__dict__).inserted_id
            # Change book possession to user
            catalog.update_one({'item_id': item_id}, {'$set': {'status': STATUS_AVAILABLE, 'possession': owner_id}})
        # TODO: add case for physical item return via 3rd party service

    pending_transactions.delete_one({'event_token': verify_token})
    return event_id


# Cancel a fulfillment request
def event_cancel(borrower_id, item_id):
    # create a new event
    owner_id = catalog.find_one({'item_id': item_id}).get('owner')
    event = Event(EVENT_CANCEL, item_id, owner_id, borrower_id)
    # add event to db
    event_id = events.insert_one(event.__dict__).inserted_id
    # change status of item in catalog
    catalog.update_one({'item_id': item_id}, {'$set': {'status': STATUS_AVAILABLE}})

    # remove pending transaction
    last_event = events.find({'item_id': item_id, 'request_type': EVENT_REQUEST}).sort('event_date', -1).next()
    pending_transactions.delete_one({'event_token': last_event.get('_id')})
    # TODO notify borrower of cancel

events.drop()
catalog.drop()
pending_transactions.drop()
isbn_test = "9788373191723"
owner_id_test = 99383
from register_item import register_item
register_item(isbn_test, owner_id_test)

test_user = users.find_one()
test_item = catalog.find_one()
event_request(test_user.get('_id'), test_item.get('item_id'))
event_cancel(test_user.get('_id'), test_item.get('item_id'))

print("Before:")
pprint(test_item)
verify = event_request(test_user.get('_id'), test_item.get('item_id'))
verify = event_transaction(verify)
print("After:")
pprint(catalog.find_one({'_id': test_item.get('_id')}))
event_transaction(verify)
print("After2:")
pprint(catalog.find_one({'_id': test_item.get('_id')}))

for trans in pending_transactions.find():
    pprint(trans)
