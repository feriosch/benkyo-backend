from flask.views import MethodView
from flask import make_response, request

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
import jap_dev.responses.word.search as responses


class WordSearchView(MethodView):
    decorators = [validate_schema('search_one_word_schema')]

    def get(self, params):
        validate_session(request)
        if 'word' in params:
            return make_response(responses.get_one_by_word_response(params['word']))
        elif 'word_id' in params:
            return make_response(responses.get_one_by_id_response(params['word_id']))
        elif 'from' in params:
            return make_response(responses.get_one_random_by_collection_response(params['from']))
        else:
            return make_response(responses.get_one_random_response())
