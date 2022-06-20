from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
import jap_dev.responses.kanji.components as responses


class KanjiComponentsView (MethodView):
    decorators = [validate_schema('kanji_components_schema')]

    def get(self, params):
        validate_session(request)
        starting = None
        limit = None
        if 'starting' in params:
            starting = params['starting']
        if 'limit' in params:
            limit = int(params['limit'])
        return make_response(responses.get_distinct_components_response(starting=starting, limit=limit))
