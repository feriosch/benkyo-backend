from flask import (jsonify)

from jap_dev.queries.collection.verify import check_if_collection_exists
from jap_dev.queries.collection.main import insert_collection
from jap_dev.formatters.collection.insert import format_collection_insertion
from jap_dev.formatters.id.main import format_response_id


def insert_collection_response(collection):
    if check_if_collection_exists(collection['collection_name']):
        return {'error': 'Repeated collection name'}, 400
    formatted_info = format_collection_insertion(collection)
    inserted_id = insert_collection(formatted_info)
    return jsonify(format_response_id(inserted_id))
