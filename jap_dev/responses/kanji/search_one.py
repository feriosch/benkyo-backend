from flask import (jsonify)
from bson.objectid import ObjectId

import jap_dev.queries.kanji.search_one as queries
from jap_dev.formatters.kanji.main import format_kanji


def get_random_kanji_response():
    result = list(queries.get_one_random())
    if not result:
        return {'error': 'No kanjis found'}, 400
    return jsonify(format_kanji(result[0]))


def get_kanji_by_id_response(kanji_id):
    if not ObjectId.is_valid(kanji_id):
        return {'error': 'Invalid ID'}, 400
    result = queries.get_one_by_id(kanji_id)
    if result is None:
        return {'error': 'No matched kanji'}, 400
    return jsonify(format_kanji(result))


def get_kanji_by_kanji_response(kanji):
    result = queries.get_one_by_kanji(kanji)
    if result is None:
        return {'error': 'No matched kanji'}, 400
    return jsonify(format_kanji(result))


def get_kanji_by_v1_response(v1):
    result = queries.get_one_by_v1(int(v1))
    if result is None:
        return {'error': 'No matched kanji'}, 400
    return jsonify(format_kanji(result))
