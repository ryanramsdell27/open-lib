from pymongo import MongoClient
from pprint import pprint

client = MongoClient()
db = client.lib
books = db.books
catalog = db.catalog
users = db.users


# Creates a new entry in the database, basic verification based on unique email
# returned object guaranteed to have just id
def get_user_id(email):
    user_check = users.find_one({'email': email})
    if user_check is not None:
        return user_check.get('_id')
    else:
        return None


class User:
    def __init__(self, name, email, phone):
        check = users.find_one({'email': email})
        if check is None:
            self.name = name
            self.email = email
            self.phone = phone
            self.id = users.insert_one(self.__dict__).inserted_id
        else:
            self.id = check.get('_id')


# users.drop()
names = ["Payton", "Ryan", "Aiden", "Mike"]
emails = ["pg@wisc.edu", "rr@wisc.edu", "as@wisc.edu", "mw@wisc.edu"]
phones = [1, 2, 3, 4]
for i in range(len(names)):
    print(User(names[i], emails[i], phones[i]).id)

for user in users.find():
    pprint(user)
