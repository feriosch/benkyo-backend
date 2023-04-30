from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.kanji.components import kanji_irregular_component_insert_schema
from jap_dev.responses.kanji.components.irregular import get_irregular_components_response
from jap_dev.responses.kanji.components.irregular import insert_irregular_component_response


class KanjiIrregularComponentsView(MethodView):
    decorators = [validate_session]

    # TODO: Schema
    def get(self):
        return make_response(get_irregular_components_response())

    @validate_schema(kanji_irregular_component_insert_schema)
    def post(self):
        return make_response(insert_irregular_component_response(get_params()))
