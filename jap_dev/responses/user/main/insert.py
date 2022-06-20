from argon2 import PasswordHasher
from flask import (jsonify)

from jap_dev.queries import user as queries
from jap_dev.formatters import user as formatter
from jap_dev.formatters import id_formatter


def insert_user_response(user):
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
