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


def get_one_random_response():
    result = list(queries.get_one_random())
    if not result:
        return {'error': 'No kanjis found'}, 400
    return jsonify(formatter.format_kanji(result[0]))


def check_if_v1_exists_response(v1):
    return jsonify(queries.check_if_v1_exists(v1))


def check_if_kanji_exists_response(kanji):
    return jsonify(queries.check_if_kanji_exists(kanji))


def check_if_spanish_exists_response(spanish):
    return jsonify(queries.check_if_spanish_exists(spanish))


def create_response(kanji_info):
    if len(kanji_info['kanji']) != 1:
        return {'error': 'Kanji should be just one character'}, 400
    if not kanji_info['spanish'] or str.isspace(kanji_info['spanish']):
        return {'error': 'Invalid spanish'}, 400
    if queries.check_if_v1_exists(kanji_info['v1']):
        return {'error': 'V1 already exists'}, 400
    if queries.check_if_kanji_exists(kanji_info['kanji']):
        return {'error': 'Kanji already exists'}, 400
    if queries.check_if_spanish_exists(kanji_info['spanish']):
        return {'error': 'Spanish already exists'}, 400
    formatted_kanji = formatter.format_kanji_insertion(kanji_info)
    if 'components' in kanji_info:
        formatted_kanji['radicals'] = queries.get_radicals(kanji_info['components'])
    else:
        formatted_kanji['radicals'] = queries.get_radicals([kanji_info['spanish']])
    inserted_id = queries.insert(formatted_kanji)
    return jsonify(id_formatter.format_response_id(inserted_id))


def update_response(kanji_info):
    if len(kanji_info['kanji']) != 1:
        return {'error': 'Kanji should be just one character'}, 400
    if not kanji_info['spanish'] or str.isspace(kanji_info['spanish']):
        return {'error': 'Invalid spanish'}, 400
    kanji_id = kanji_info['kanji_id']
    formatted_kanji = formatter.format_kanji_insertion(kanji_info)
    deleted_fields = formatter.format_deleted_fields(kanji_info)
    if 'components' in kanji_info:
        formatted_kanji['radicals'] = queries.get_radicals(kanji_info['components'])
    else:
        formatted_kanji['radicals'] = queries.get_radicals([kanji_info['spanish']])
    if deleted_fields:
        return jsonify(queries.update_kanji_deleting_fields(kanji_id, deleted_fields, formatted_kanji))
    else:
        return jsonify(queries.update_kanji(kanji_id, formatted_kanji))


def get_distinct_components_response(starting=None, limit=None):
    components = list(queries.get_distinct_components())
    if starting:
        components = list(filter(lambda x: x.startswith(starting), queries.get_distinct_components()))
    if limit:
        components = components[:limit]
    return jsonify(components)
