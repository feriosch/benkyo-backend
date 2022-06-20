from flask import (jsonify)

from jap_dev.queries import word as queries
from jap_dev.formatters import word as formatter


def search_many_words_response(word):
    result = queries.search_many(word)
    return jsonify(formatter.format_all_words(result))
