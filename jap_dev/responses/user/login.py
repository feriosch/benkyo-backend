from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from flask import (jsonify)

from jap_dev.queries.user.search import get_one_by_username
from jap_dev.formatters.user.login import format_token_claims, format_login_response
from jap_dev.helpers.token import generate_token


def user_login_response(user):
    # Verify if password is valid, compare with the one stored in db
    user_info = get_one_by_username(user['username'])
    if user_info is None:
        return {'error': 'Incorrect username or password'}, 400
    ph = PasswordHasher()
    try:
        ph.verify(user_info['password'], user['password'])
    except VerifyMismatchError:
        return {'error': 'Incorrect username or password'}, 400
    # If it is correct, generate JWT
    token = generate_token(format_token_claims(
        user_info,
        (datetime.utcnow() + timedelta(hours=24))
    ))
    # Return user info along with JWT
    return jsonify(format_login_response(user_info, token))
