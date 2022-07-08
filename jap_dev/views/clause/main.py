from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.clause.main.get import clause_get_schema
from jap_dev.schemas.clause.main.insert import clause_insert_schema
from jap_dev.responses.clause.main.get import get_clauses_response
from jap_dev.responses.clause.main.insert import insert_clause_response


class ClauseMainView(MethodView):
    decorators = [validate_session]

    @validate_schema(clause_get_schema)
    def get(self):
        return make_response(get_clauses_response(get_params()))

    @validate_schema(clause_insert_schema)
    def post(self):
        return make_response(insert_clause_response(get_params()))
