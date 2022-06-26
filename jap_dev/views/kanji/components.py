from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.kanji.components import kanji_components_schema
import jap_dev.responses.kanji.components as responses


class KanjiComponentsView (MethodView):
    decorators = [validate_session]

    @validate_schema(kanji_components_schema)
    def get(self):
        params = get_params()
        starting = None
        limit = None
        if 'starting' in params:
            starting = params['starting']
        if 'limit' in params:
            limit = int(params['limit'])
        return make_response(responses.get_distinct_components_response(starting=starting, limit=limit))
