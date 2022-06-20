from flask import make_response
from flask.views import MethodView

from jap_dev.helpers.validation import validate_schema
import jap_dev.responses.user.login as responses


class UserLoginView(MethodView):
    decorators = [validate_schema('login_schema')]

    def post(self, body):
        return make_response(responses.user_login_response(body))
