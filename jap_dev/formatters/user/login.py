def _format_id(user_id):
    return str(user_id)


def _clean_password(user):
    del user['password']
    return user


def _format_id_plug(user):
    user['id'] = _format_id(user['_id'])
    del user['_id']
    return user


def format_token_claims(user, expiration_date):
    cleaned_user = _clean_password(user)
    cleaned_user = _format_id_plug(cleaned_user)
    cleaned_user['exp'] = expiration_date
    return cleaned_user


def format_login_response(user, token):
    user['token'] = token
    return user
