from flask import (jsonify)

import jap_dev.queries.kanji.verify as queries


def check_if_v1_exists_response(v1):
    return jsonify(queries.check_if_v1_exists(v1))


def check_if_kanji_exists_response(kanji):
    return jsonify(queries.check_if_kanji_exists(kanji))


def check_if_spanish_exists_response(spanish):
    return jsonify(queries.check_if_spanish_exists(spanish))
