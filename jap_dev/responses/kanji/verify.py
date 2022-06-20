from flask import (jsonify)

from jap_dev.queries import kanji as queries


def check_if_v1_exists_response(v1):
    return jsonify(queries.check_if_v1_exists(v1))


def check_if_kanji_exists_response(kanji):
    return jsonify(queries.check_if_kanji_exists(kanji))


def check_if_spanish_exists_response(spanish):
    return jsonify(queries.check_if_spanish_exists(spanish))
