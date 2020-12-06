from flask import (jsonify)

from jap_dev.queries import group_collection as queries
from jap_dev.formatters import group_collection as formatter
from jap_dev.formatters import id_formatter


def get_response():
    result = queries.get_all()
    return jsonify(formatter.format_all(result))


def create_response(collection):
    if queries.check_if_exists(collection['collection_name']):
        return {'error': 'Repeated collection name'}, 400
    formatted_info = formatter.format_insertion(collection)
    inserted_id = queries.insert(formatted_info)
    return jsonify(id_formatter.format_response_id(inserted_id))
