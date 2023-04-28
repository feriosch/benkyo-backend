from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.kanji.components import kanji_components_schema
import jap_dev.responses.kanji.radicals as responses


class KanjiRadicalsView(MethodView):
    decorators = [validate_session]

    @validate_schema(kanji_components_schema)
    def get(self):
        return make_response(responses.get_distinct_radicals_response(get_params()))
