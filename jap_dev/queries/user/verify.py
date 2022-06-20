from jap_dev.information import users


def check_if_username_exists(username):
    return users().find({'username': username}).count() > 0
