from flask import (jsonify)

from jap_dev.queries.kanji.components import get_distinct_components


def get_distinct_components_response(starting=None, limit=None):
    components = list(get_distinct_components())
    if starting:
        components = list(filter(lambda x: x.startswith(starting), get_distinct_components()))
    if limit:
        components = components[:limit]
    return jsonify(components)
