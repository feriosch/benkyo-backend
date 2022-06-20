from flask import (jsonify)

from jap_dev.queries.word.search_many import search_many
from jap_dev.formatters.word.main import format_all_words


def search_many_words_response(word):
    result = search_many(word)
    return jsonify(format_all_words(result))
