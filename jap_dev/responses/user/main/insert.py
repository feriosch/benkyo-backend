from argon2 import PasswordHasher
from flask import (jsonify)

from jap_dev.queries.user.verify import check_if_username_exists
from jap_dev.queries.user.main import insert_user
from jap_dev.formatters.user.insert import format_user_insertion
from jap_dev.formatters.id.main import format_response_id


def insert_user_response(user):
    # Create salted password
    ph = PasswordHasher()
    hashed = ph.hash(user['password'])
    # Format user for insertion
    formatted_user = format_user_insertion(user, hashed)
    # Query insert user
    if check_if_username_exists(user['username']):
        return {'error': 'Username already exists'}, 400
    inserted_id = insert_user(formatted_user).inserted_id
    # Return id
    return jsonify(format_response_id(inserted_id))
