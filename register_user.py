from pymongo import MongoClient
from pprint import pprint
from utils import books, catalog, users


# Returns the user id associated with an email
def get_user_id(email):
    user_check = users.find_one({'email': email})
    if user_check is not None:
        return user_check.get('_id')
    else:
        return None


# Creates a new user, returns the id
def register_user(name, email, phone):
    user_temp = User(name, email, phone)
    return user_temp.id


# If a user does not exist in the db create it, otherwise get's id of current entry
# TODO what if user enters different name and phone from current entry but same email
class User:
    def __init__(self, name, email, phone):
        check = users.find_one({'email': email})
        self.name = name
        self.email = email
        self.phone = phone
        if check is None:
            self.id = users.insert_one(self.__dict__).inserted_id
        else:
            self.id = check.get('_id')


# users.drop()
# names = ["Payton Garland", "Ryan", "Aiden", "Mike"]
# emails = ["payton.r.g@gmail.com", "rr@wisc.edu", "as@wisc.edu", "mw@wisc.edu"]
# phones = [6083453222, 2, 3, 4]
# for i in range(len(names)):
#     print(register_user(names[i], emails[i], phones[i]))

# for user in users.find():
#     pprint(user)
