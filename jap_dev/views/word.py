from flask.views import MethodView
from flask import (make_response)

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import authenticate_jwt
from jap_dev.responses import word


class Word (MethodView):
    decorators = [authenticate_jwt(), validate_schema('word_schema')]

    def get(self, params):
        if 'from' in params:
            return make_response(word.get_from_collection_response(params['from']))
        return make_response(word.get_all_response())

    def post(self, body):
        return make_response(word.create_word_response(body))

    def put(self, body):
        return make_response(word.update_word_response(body))


class SearchOne (MethodView):
    decorators = [authenticate_jwt(), validate_schema('search_one_word_schema')]

    def get(self, params):
        if 'word' in params:
            return make_response(word.search_one_by_word_response(params['word']))
        elif 'word_id' in params:
            return make_response(word.search_one_by_id_response(params['word_id']))


class SearchMany (MethodView):
    decorators = [authenticate_jwt(), validate_schema('search_word_schema')]

    def get(self, params):
        return make_response(word.search_many_response(params['word']))


class UpdateLevel (MethodView):
    decorators = [authenticate_jwt(), validate_schema('update_word_level_schema')]

    def put(self, body):
        return make_response(word.update_level_response(body['word_id'], body['success']))
