from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
from flask import (jsonify)

from jap_dev.queries import user as queries
from jap_dev.formatters import user as formatter
from jap_dev.formatters import id_formatter
from jap_dev.helpers.token import generate_token


def get_response():
    result = queries.get_all()
    return jsonify(formatter.format_all_users(result))


def create_response(user):
    # Create salted password
    ph = PasswordHasher()
    hashed = ph.hash(user['password'])
    # Format user for insertion
    formatted_user = formatter.format_user_insertion(user, hashed)
    # Query insert user
    if queries.get_info_from_username(user['username']) is None:
        inserted_id = queries.insert(formatted_user).inserted_id
    else:
        return {'error': 'Username already exists'}, 400
    # Return id
    return jsonify(id_formatter.format_response_id(inserted_id))


def login_response(user):
    # Verify if password is valid, compare with the one stored in db
    user_info = queries.get_info_from_username(user['username'])
    if user_info is None:
        return {'error': 'Incorrect username or password'}, 400
    ph = PasswordHasher()
    try:
        ph.verify(user_info['password'], user['password'])
    except VerifyMismatchError:
        return {'error': 'Incorrect username or password'}, 400
    # If it is correct, generate JWT
    token = generate_token(formatter.format_token_claims(
        user_info,
        (datetime.utcnow() + timedelta(hours=12))
    ))
    # Return user info along with JWT
    return jsonify(formatter.format_login_response(user_info, token))
