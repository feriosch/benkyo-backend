from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import kanji


class MainKanjiView(MethodView):
    decorators = [validate_schema('kanji_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(kanji.get_kanjis_response(params))

    def post(self, body):
        validate_session(request)
        return make_response(kanji.create_response(body))

    def put(self, body):
        validate_session(request)
        return make_response(kanji.update_response(body))
