from flask import (jsonify)

from jap_dev.queries import word as queries
from jap_dev.formatters import word as formatter
from jap_dev.formatters import id_formatter


def get_all_response():
    result = queries.get_all()
    return jsonify(formatter.format_all_words(result))


def get_from_collection_response(collection):
    if collection == 'all':
        result = queries.get_all()
    else:
        result = queries.get_words_from(collection)
    return jsonify(formatter.format_all_words(result))


def create_word_response(word_info):
    if queries.check_if_exists(word_info['word']):
        return {'error': 'Word repeated'}, 400
    if word_info['from'] == 'all':
        return {'error': 'Bad collection input: all is not allowed'}, 400
    formatted_word = formatter.format_word_insertion(word_info)
    inserted_id = queries.insert(formatted_word)
    return jsonify(id_formatter.format_response_id(inserted_id))


def search_one_response(word):
    result = queries.search_one(word)
    return jsonify(formatter.format_all_words(result))


def search_many_response(word):
    result = queries.search_many(word)
    return jsonify(formatter.format_all_words(result))


def update_word_response(word_info):
    word_id = word_info['word_id']
    formatted_word = formatter.format_word_update(word_info)
    if queries.update_word(word_id, formatted_word):
        return {'id': word_id}, 200
    return {'error': 'No matched word'}, 400


def update_level_response(word_id, success):
    bool_success = bool(int(success))
    if queries.update_word_level(word_id, bool_success):
        return {'id': word_id}, 200
    return {'error': 'No matched word'}, 400
