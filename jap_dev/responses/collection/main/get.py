from flask import (jsonify)

from jap_dev.queries.collection.main import get_collections
from jap_dev.queries.collection.search import get_collection_by_name
from jap_dev.formatters import group_collection as formatter


def get_collections_response(params):
    if 'name' in params:
        name = params['name']
        result = get_collection_by_name(name)
        if result:
            return jsonify(formatter.format_one(result))
        return {'error': 'Collection not found'}, 404
    else:
        result = get_collections()
        return jsonify(formatter.format_all(result))
