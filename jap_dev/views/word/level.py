from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.word.level import word_level_update_schema
import jap_dev.responses.word.level as responses


class WordLevelView(MethodView):
    decorators = [validate_session]

    @validate_schema(word_level_update_schema)
    def put(self):
        params = get_params()
        return make_response(responses.update_level_response(params['word_id'], params['success']))
