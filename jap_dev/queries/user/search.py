from bson.objectid import ObjectId

from jap_dev.information import users


def get_one_by_id(user_id):
    return users().find_one({'_id': ObjectId(user_id)})


def get_one_by_username(username):
    return users().find_one({'username': username})
