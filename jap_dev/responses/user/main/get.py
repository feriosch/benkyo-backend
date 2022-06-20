from flask import (jsonify)

from jap_dev.queries import user as queries
from jap_dev.formatters import user as formatter


def get_users_response():
    result = queries.get_all()
    return jsonify(formatter.format_all_users(result))
