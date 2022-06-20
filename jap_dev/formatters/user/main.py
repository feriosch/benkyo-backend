def format_user(user):
    return {
        # 'id': user['_id'],
        'username': user['username']
    }


def format_all_users(users):
    result = []
    for user in users:
        result.append(format_user(user))
    return result
