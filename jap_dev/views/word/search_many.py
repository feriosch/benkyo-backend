from flask.views import MethodView
from flask import make_response, request

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import word


class SearchManyWordsView(MethodView):
    decorators = [validate_schema('search_word_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(word.search_many_response(params['word']))
