from flask import (jsonify)

from jap_dev.queries import kanji as queries


def get_distinct_components_response(starting=None, limit=None):
    components = list(queries.get_distinct_components())
    if starting:
        components = list(filter(lambda x: x.startswith(starting), queries.get_distinct_components()))
    if limit:
        components = components[:limit]
    return jsonify(components)
