from flask import (jsonify)

from jap_dev.queries import kanji as queries
from jap_dev.formatters import kanji as formatter
from jap_dev.formatters import id_formatter


def insert_kanji_response(kanji_info):
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
