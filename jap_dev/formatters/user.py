def _format_id(user_id):
    return str(user_id)


def _clean_password(user):
    del user['password']
    return user


def _format_id_plug(user):
    user['id'] = _format_id(user['_id'])
    del user['_id']
    return user


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


def format_user_insertion(user, password):
    return {
        'username': user['username'],
        'password': password,
        'type': user['type']
    }


def format_token_claims(user, expiration_date):
    cleaned_user = _clean_password(user)
    cleaned_user = _format_id_plug(cleaned_user)
    cleaned_user['exp'] = expiration_date
    return cleaned_user


def format_login_response(user, token):
    user['token'] = token
    return user
