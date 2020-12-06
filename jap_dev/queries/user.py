from bson.objectid import ObjectId

from jap_dev.information import users


def get_all():
    return users().find()


def get_info_from_id(user_id):
    return users().find_one({'_id': ObjectId(user_id)})


def get_info_from_username(username):
    return users().find_one({'username': username})


def insert(user):
    return users().insert_one(user)
