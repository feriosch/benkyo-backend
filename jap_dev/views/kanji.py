from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import kanji


class Kanji (MethodView):
    decorators = [validate_schema('kanji_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(kanji.get_with_components_response(params))

    def post(self, body):
        validate_session(request)
        return make_response(kanji.create_response(body))

    def put(self, body):
        validate_session(request)
        return make_response(kanji.update_response(body))


class SearchOne(MethodView):
    decorators = [validate_schema('search_one_kanji_schema')]

    def get(self, params):
        validate_session(request)
        if 'kanji_id' in params:
            return make_response(kanji.get_one_by_id_response(params['kanji_id']))
        return make_response(kanji.get_one_random_response())


class VerifyExistence (MethodView):
    decorators = [validate_schema('exists_kanji_schema')]

    def get(self, params):
        validate_session(request)
        if 'v1' in params:
            return make_response(kanji.check_if_v1_exists_response(int(params['v1'])))
        elif 'kanji' in params:
            return make_response(kanji.check_if_kanji_exists_response(params['kanji']))
        elif 'spanish' in params:
            return make_response(kanji.check_if_spanish_exists_response(params['spanish']))
        else:
            return make_response({'error': 'Invalid params'}, 400)


class Components (MethodView):
    decorators = [validate_schema('kanji_components_schema')]

    def get(self, params):
        validate_session(request)
        starting = None
        limit = None
        if 'starting' in params:
            starting = params['starting']
        if 'limit' in params:
            limit = int(params['limit'])
        return make_response(kanji.get_distinct_components_response(starting=starting, limit=limit))
