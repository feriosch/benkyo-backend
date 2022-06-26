from flask.views import MethodView
from flask import make_response, request

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.word.main.get import word_get_schema
from jap_dev.responses.word.main.get import get_words_response
from jap_dev.responses.word.main.insert import insert_word_response
from jap_dev.responses.word.main.update import update_word_response
from jap_dev.responses.word.main.delete import delete_word_response


class WordMainView(MethodView):
    decorators = [validate_session]

    @validate_schema(schema=word_get_schema)
    def get(self):
        return make_response(get_words_response(get_params()))

    def post(self, body):
        validate_session(request)
        return make_response(insert_word_response(body))

    def put(self, body):
        validate_session(request)
        return make_response(update_word_response(body))

    def delete(self, params):
        validate_session(request)
        return make_response(delete_word_response(params))
