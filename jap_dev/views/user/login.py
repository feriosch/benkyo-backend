from flask import make_response
from flask.views import MethodView

from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.user.login import user_login_schema
import jap_dev.responses.user.login as responses


class UserLoginView(MethodView):

    @validate_schema(user_login_schema)
    def post(self):
        return make_response(responses.user_login_response(get_params()))
