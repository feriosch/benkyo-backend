from flask import make_response
from flask.views import MethodView

from jap_dev.helpers.validation import validate_schema
from jap_dev.responses.user.main.get import get_users_response
from jap_dev.responses.user.main.insert import insert_user_response


class MainUserView(MethodView):
    decorators = [validate_schema('user_schema')]

    def get(self, _params):
        return make_response(get_users_response())

    def post(self, body):
        return make_response(insert_user_response(body))
