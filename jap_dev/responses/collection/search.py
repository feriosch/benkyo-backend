from flask import jsonify

import jap_dev.queries.collection.search as queries
from jap_dev.formatters.collection.main import format_collection


def get_one_collection_by_name_response(name):
    result = queries.get_collection_by_name(name)
    if result is None:
        return {'error': 'No matched clause'}, 400
    return jsonify(format_collection(result))
