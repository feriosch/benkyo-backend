from jap_dev.information import users


def get_users():
    return users().find()


def insert_user(user):
    return users().insert_one(user)
