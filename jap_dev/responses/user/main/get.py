from flask import (jsonify)

from jap_dev.queries.user.main import get_users
from jap_dev.formatters.user.main import format_all_users


def get_users_response():
    result = get_users()
    return jsonify(format_all_users(result))
