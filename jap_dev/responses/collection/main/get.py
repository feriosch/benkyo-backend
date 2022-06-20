from flask import (jsonify)

from jap_dev.queries.collection.main import get_collections
from jap_dev.queries.collection.search import get_collection_by_name
from jap_dev.formatters.collection.main import format_collection, format_all_collections


def get_collections_response(params):
    if 'name' in params:
        name = params['name']
        result = get_collection_by_name(name)
        if result:
            return jsonify(format_collection(result))
        return {'error': 'Collection not found'}, 404
    else:
        result = get_collections()
        return jsonify(format_all_collections(result))
