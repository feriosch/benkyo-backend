from flask import (jsonify)

from jap_dev.queries import group_collection as queries
from jap_dev.formatters import group_collection as formatter
from jap_dev.formatters import id_formatter


def get_response(params):
    if 'name' in params:
        name = params['name']
        result = queries.get_collection_by_name(name)
        if result:
            return jsonify(formatter.format_one(result))
        return {'error': 'Collection not found'}, 404
    else:
        result = queries.get_all()
        return jsonify(formatter.format_all(result))


def create_response(collection):
    if queries.check_if_exists(collection['collection_name']):
        return {'error': 'Repeated collection name'}, 400
    formatted_info = formatter.format_insertion(collection)
    inserted_id = queries.insert(formatted_info)
    return jsonify(id_formatter.format_response_id(inserted_id))
