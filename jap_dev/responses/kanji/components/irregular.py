from flask import (jsonify)

import jap_dev.queries.kanji.components.irregular as queries
from jap_dev.formatters.kanji.components import format_all_irregular_components
from jap_dev.formatters.kanji.components import format_irregular_component_insertion
from jap_dev.formatters.id.main import format_response_id


def get_irregular_components_response():
    # TODO: Pagination params
    components = queries.get_irregular_components()
    formatted_components = format_all_irregular_components(components)
    return {
        'components': formatted_components
    }


def insert_irregular_component_response(component_info):
    if queries.check_if_component_exists(component_info['component']):
        return {'error': 'Component already exists'}, 400
    if len(component_info['radicals']) < 1:
        return {'error': 'No radicals found'}, 400
    if len(component_info['radicals']) > 6:
        return {'error': 'Too many radicals'}, 400
    formatted_component = format_irregular_component_insertion(component_info)
    inserted_id = queries.insert_irregular_component(formatted_component)
    return jsonify(format_response_id(inserted_id))
