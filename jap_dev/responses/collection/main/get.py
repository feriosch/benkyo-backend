from flask import (jsonify)

from jap_dev.queries import group_collection as queries
from jap_dev.formatters import group_collection as formatter


def get_collections_response(params):
    if 'name' in params:
        name = params['name']
        result = queries.get_collection_by_name(name)
        if result:
            return jsonify(formatter.format_one(result))
        return {'error': 'Collection not found'}, 404
    else:
        result = queries.get_all()
        return jsonify(formatter.format_all(result))
