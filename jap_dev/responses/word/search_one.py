from flask import (jsonify)
from bson.objectid import ObjectId

import jap_dev.queries.word.search_one as queries
from jap_dev.formatters.word.main import format_word


def get_one_random_response():
    result = list(queries.search_one_random())
    if not result:
        return {'error': 'No words found'}, 400
    return jsonify(format_word(result[0]))


def get_one_by_id_response(word_id):
    if not ObjectId.is_valid(word_id):
        return {'error': 'Invalid ID'}, 400
    result = queries.search_one_by_id(word_id)
    if result is None:
        return {'error': 'No matched word'}, 400
    return jsonify(format_word(result))


def get_one_by_word_response(word):
    result = queries.search_one_by_word(word)
    if result is None:
        return jsonify(result)
    return jsonify(format_word(result))


def get_one_random_by_collection_response(collection):
    result = list(queries.search_one_random_by_collection(collection))
    if not result:
        return {'error': 'No words found in collection'}, 400
    return jsonify(format_word(result[0]))
