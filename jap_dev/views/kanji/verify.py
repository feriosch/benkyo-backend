from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.kanji.verify import kanji_exists_schema
import jap_dev.responses.kanji.verify as responses


class VerifyKanjiExistenceView(MethodView):
    decorators = [validate_session]

    @validate_schema(kanji_exists_schema)
    def get(self):
        params = get_params()
        if 'v1' in params:
            return make_response(responses.check_if_v1_exists_response(int(params['v1'])))
        elif 'kanji' in params:
            return make_response(responses.check_if_kanji_exists_response(params['kanji']))
        elif 'spanish' in params:
            return make_response(responses.check_if_spanish_exists_response(params['spanish']))
        else:
            return make_response({'error': 'Invalid params'}, 400)
