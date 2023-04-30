from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
import jap_dev.responses.kanji.components.irregular as responses


class KanjiIrregularComponentsView(MethodView):
    decorators = [validate_session]

    # TODO: Schema
    def get(self):
        return make_response(responses.get_irregular_components_response())
