from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.kanji.search import kanji_search_one_schema
import jap_dev.responses.kanji.search_one as responses


class SearchKanjiView(MethodView):
    decorators = [validate_session]

    @validate_schema(kanji_search_one_schema)
    def get(self):
        params = get_params()
        if 'kanji_id' in params:
            return make_response(responses.get_kanji_by_id_response(params['kanji_id']))
        elif 'kanji' in params:
            return make_response(responses.get_kanji_by_kanji_response(params['kanji']))
        elif 'v1' in params:
            return make_response(responses.get_kanji_by_v1_response(params['v1']))
        return make_response(responses.get_random_kanji_response())
