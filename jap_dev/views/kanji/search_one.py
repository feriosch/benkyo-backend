from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
import jap_dev.responses.kanji.search_one as responses


class SearchOneKanjiView(MethodView):
    decorators = [validate_schema('search_one_kanji_schema')]

    def get(self, params):
        validate_session(request)
        if 'kanji_id' in params:
            return make_response(responses.get_kanji_by_id_response(params['kanji_id']))
        elif 'kanji' in params:
            return make_response(responses.get_kanji_by_kanji_response(params['kanji']))
        return make_response(responses.get_random_kanji_response())
