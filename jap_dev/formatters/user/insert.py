def format_user_insertion(user, password):
    return {
        'username': user['username'],
        'password': password,
        'type': user['type']
    }
