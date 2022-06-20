from flask import (jsonify)

from jap_dev.queries.word.verify import check_if_word_exists
from jap_dev.queries.word.main import insert_word
from jap_dev.formatters import word as formatter
from jap_dev.formatters import id_formatter


def insert_word_response(word_info):
    if check_if_word_exists(word_info['word']):
        return {'error': 'Word repeated'}, 400
    if word_info['from'] == 'all':
        return {'error': 'Bad collection input: all is not allowed'}, 400
    formatted_word = formatter.format_word_insertion(word_info)
    inserted_id = insert_word(formatted_word)
    return jsonify(id_formatter.format_response_id(inserted_id))
