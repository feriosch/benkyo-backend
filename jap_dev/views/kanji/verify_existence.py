from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import kanji


class VerifyKanjiExistenceView(MethodView):
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
