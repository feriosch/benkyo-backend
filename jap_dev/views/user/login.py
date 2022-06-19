from flask import make_response
from flask.views import MethodView

from jap_dev.helpers.validation import validate_schema
from jap_dev.responses import user


class UserLoginView(MethodView):
    decorators = [validate_schema('login_schema')]

    def post(self, body):
        return make_response(user.login_response(body))
