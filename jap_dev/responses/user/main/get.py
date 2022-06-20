from flask import (jsonify)

from jap_dev.queries.user.main import get_users
from jap_dev.formatters import user as formatter


def get_users_response():
    result = get_users()
    return jsonify(formatter.format_all_users(result))
