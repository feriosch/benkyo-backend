from argon2 import PasswordHasher
from flask import (jsonify)

from jap_dev.queries.user.verify import check_if_username_exists
from jap_dev.queries.user.main import insert_user
from jap_dev.formatters import user as formatter
from jap_dev.formatters import id_formatter


def insert_user_response(user):
    # Create salted password
    ph = PasswordHasher()
    hashed = ph.hash(user['password'])
    # Format user for insertion
    formatted_user = formatter.format_user_insertion(user, hashed)
    # Query insert user
    if check_if_username_exists(user['username']):
        return {'error': 'Username already exists'}, 400
    inserted_id = insert_user(formatted_user).inserted_id
    # Return id
    return jsonify(id_formatter.format_response_id(inserted_id))
