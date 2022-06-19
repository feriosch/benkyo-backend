from flask.views import MethodView
from flask import make_response, request

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import word


class UpdateWordLevelView(MethodView):
    decorators = [validate_schema('update_word_level_schema')]

    def put(self, body):
        validate_session(request)
        return make_response(word.update_level_response(body['word_id'], body['success']))
