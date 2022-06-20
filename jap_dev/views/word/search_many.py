from flask.views import MethodView
from flask import make_response, request

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
import jap_dev.responses.word.search_many as responses


class SearchManyWordsView(MethodView):
    decorators = [validate_schema('search_word_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(responses.search_many_words_response(params['word']))
