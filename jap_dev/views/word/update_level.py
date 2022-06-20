from flask.views import MethodView
from flask import make_response, request

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
import jap_dev.responses.word.update_level as responses


class UpdateWordLevelView(MethodView):
    decorators = [validate_schema('update_word_level_schema')]

    def put(self, body):
        validate_session(request)
        return make_response(responses.update_level_response(body['word_id'], body['success']))
