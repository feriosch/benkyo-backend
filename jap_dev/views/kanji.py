from flask.views import MethodView
from flask import (make_response)

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import authenticate_jwt
from jap_dev.responses import kanji


class Kanji (MethodView):
    decorators = [authenticate_jwt(), validate_schema('kanji_schema')]

    def get(self, params):
        return make_response(kanji.get_with_components_response(params))

    def post(self, body):
        return make_response(kanji.create_response(body))
