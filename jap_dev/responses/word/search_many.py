from flask import (jsonify)

from jap_dev.queries.word.search_many import search_many
from jap_dev.formatters import word as formatter


def search_many_words_response(word):
    result = search_many(word)
    return jsonify(formatter.format_all_words(result))
