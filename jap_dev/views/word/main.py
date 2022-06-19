from flask.views import MethodView
from flask import make_response, request

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import word


class MainWordView(MethodView):
    decorators = [validate_schema('word_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(word.get_words_response(params))

    def post(self, body):
        validate_session(request)
        return make_response(word.create_word_response(body))

    def put(self, body):
        validate_session(request)
        return make_response(word.update_word_response(body))

    def delete(self, params):
        validate_session(request)
        return make_response(word.delete_word_response(params))
