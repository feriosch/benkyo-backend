from flask import (jsonify)

import jap_dev.queries.kanji.verify as verify_queries
from jap_dev.queries.kanji.radicals import get_radicals
from jap_dev.queries.kanji.main import insert_kanji
from jap_dev.formatters.kanji.insert import format_kanji_insertion
from jap_dev.formatters.id.main import format_response_id


def insert_kanji_response(kanji_info):
    if len(kanji_info['kanji']) != 1:
        return {'error': 'Kanji should be just one character'}, 400
    if not kanji_info['spanish'] or str.isspace(kanji_info['spanish']):
        return {'error': 'Invalid spanish'}, 400
    if verify_queries.check_if_v1_exists(kanji_info['v1']):
        return {'error': 'V1 already exists'}, 400
    if verify_queries.check_if_kanji_exists(kanji_info['kanji']):
        return {'error': 'Kanji already exists'}, 400
    if verify_queries.check_if_spanish_exists(kanji_info['spanish']):
        return {'error': 'Spanish already exists'}, 400
    formatted_kanji = format_kanji_insertion(kanji_info)
    if 'components' in kanji_info:
        formatted_kanji['radicals'] = get_radicals(kanji_info['components'])
    else:
        formatted_kanji['radicals'] = get_radicals([kanji_info['spanish']])
    inserted_id = insert_kanji(formatted_kanji)
    return jsonify(format_response_id(inserted_id))
