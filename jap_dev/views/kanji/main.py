from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.kanji.main.get import kanji_get_schema
from jap_dev.schemas.kanji.main.insert import kanji_insert_schema
from jap_dev.schemas.kanji.main.update import kanji_update_schema
from jap_dev.responses.kanji.main.get import get_kanji_response
from jap_dev.responses.kanji.main.insert import insert_kanji_response
from jap_dev.responses.kanji.main.update import update_kanji_response


class MainKanjiView(MethodView):
    decorators = [validate_session]

    @validate_schema(kanji_get_schema)
    def get(self):
        return make_response(get_kanji_response(get_params()))

    @validate_schema(kanji_insert_schema)
    def post(self):
        return make_response(insert_kanji_response(get_params()))

    @validate_schema(kanji_update_schema)
    def put(self):
        return make_response(update_kanji_response(get_params()))
