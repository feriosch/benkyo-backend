from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.clause.search import search_clause_schema
import jap_dev.responses.clause.search as responses


class ClauseSearchView(MethodView):
    decorators = [validate_session]

    @validate_schema(search_clause_schema)
    def get(self):
        params = get_params()
        return make_response(responses.get_one_clause_by_id_response(params['clause_id']))
