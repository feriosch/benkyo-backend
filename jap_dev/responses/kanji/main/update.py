from flask import (jsonify)

from jap_dev.queries.kanji.radicals import get_radicals
from jap_dev.queries.kanji.main import update_kanji, update_kanji_deleting_fields
from jap_dev.formatters import kanji as formatter


def update_kanji_response(kanji_info):
    if len(kanji_info['kanji']) != 1:
        return {'error': 'Kanji should be just one character'}, 400
    if not kanji_info['spanish'] or str.isspace(kanji_info['spanish']):
        return {'error': 'Invalid spanish'}, 400
    kanji_id = kanji_info['kanji_id']
    formatted_kanji = formatter.format_kanji_insertion(kanji_info)
    deleted_fields = formatter.format_deleted_fields(kanji_info)
    if 'components' in kanji_info:
        formatted_kanji['radicals'] = get_radicals(kanji_info['components'])
    else:
        formatted_kanji['radicals'] = get_radicals([kanji_info['spanish']])
    if deleted_fields:
        return jsonify(update_kanji_deleting_fields(kanji_id, deleted_fields, formatted_kanji))
    else:
        return jsonify(update_kanji(kanji_id, formatted_kanji))
