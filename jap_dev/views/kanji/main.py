from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses.kanji.main.get import get_kanji_response
from jap_dev.responses.kanji.main.insert import insert_kanji_response
from jap_dev.responses.kanji.main.update import update_kanji_response


class MainKanjiView(MethodView):
    decorators = [validate_schema('kanji_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(get_kanji_response(params))

    def post(self, body):
        validate_session(request)
        return make_response(insert_kanji_response(body))

    def put(self, body):
        validate_session(request)
        return make_response(update_kanji_response(body))
