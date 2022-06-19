from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import kanji


class SearchOneKanjiView(MethodView):
    decorators = [validate_schema('search_one_kanji_schema')]

    def get(self, params):
        validate_session(request)
        if 'kanji_id' in params:
            return make_response(kanji.get_one_by_id_response(params['kanji_id']))
        elif 'kanji' in params:
            return make_response(kanji.get_one_by_kanji(params['kanji']))
        return make_response(kanji.get_one_random_response())
