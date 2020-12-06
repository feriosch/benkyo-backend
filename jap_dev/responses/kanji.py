from flask import (jsonify)

from jap_dev.queries import kanji as queries
from jap_dev.formatters import kanji as formatter
from jap_dev.formatters import id_formatter


def get_with_components_response(parameters):
    components = []
    if 'component_1' in parameters:
        components.append(parameters['component_1'])
    if 'component_2' in parameters:
        components.append(parameters['component_2'])
    if 'component_3' in parameters:
        components.append(parameters['component_3'])
    if 'component_4' in parameters:
        components.append(parameters['component_4'])
    if 'component_5' in parameters:
        components.append(parameters['component_5'])
    if components:
        result = queries.get_from_components(components)
    else:
        result = queries.get_all()
    return jsonify(formatter.format_all_kanjis(result))


def create_response(kanji_info):
    if len(kanji_info['kanji']) != 1:
        return {'error': 'Kanji should be just one character'}, 400
    if queries.check_if_kanji_exists(kanji_info['kanji']):
        return {'error': 'Kanji already exists'}, 400
    if queries.check_if_spanish_exists(kanji_info['spanish']):
        return {'error': 'Spanish already exists'}, 400
    formatted_kanji = formatter.format_kanji_insertion(kanji_info)
    inserted_id = queries.insert(formatted_kanji)
    return jsonify(id_formatter.format_response_id(inserted_id))
