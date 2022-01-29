from flask.views import MethodView
from flask import make_response, request, send_from_directory

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import word


class Word (MethodView):
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


class SearchOne (MethodView):
    decorators = [validate_schema('search_one_word_schema')]

    def get(self, params):
        validate_session(request)
        if 'word' in params:
            return make_response(word.search_one_by_word_response(params['word']))
        elif 'word_id' in params:
            return make_response(word.search_one_by_id_response(params['word_id']))
        elif 'from' in params:
            return make_response(word.search_one_random_by_collection_response(params['from']))
        else:
            return make_response(word.search_one_random_response())


class SearchMany (MethodView):
    decorators = [validate_schema('search_word_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(word.search_many_response(params['word']))


class UpdateLevel (MethodView):
    decorators = [validate_schema('update_word_level_schema')]

    def put(self, body):
        validate_session(request)
        return make_response(word.update_level_response(body['word_id'], body['success']))


class CSV (MethodView):
    decorators = [validate_schema('word_schema')]

    def get(self, params):
        validate_session(request)
        if 'from' in params:
            collection = params['from']
            csv_response = word.csv_response(collection)
            if csv_response:
                return send_from_directory('files', f'{collection}.csv', as_attachment=True)
            else:
                return {'error': 'Error processing CSV file.'}, 500
        else:
            csv_response = word.csv_response(None)
            if csv_response:
                return send_from_directory('files', 'benkyo.csv', as_attachment=True)
            return {'error': 'Error processing CSV file.'}, 500
