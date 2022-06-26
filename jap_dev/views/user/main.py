from flask import make_response
from flask.views import MethodView

from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.user.main.get import user_get_schema
from jap_dev.schemas.user.main.insert import user_insert_schema
from jap_dev.responses.user.main.get import get_users_response
from jap_dev.responses.user.main.insert import insert_user_response


class MainUserView(MethodView):

    @validate_schema(user_get_schema)
    def get(self):
        return make_response(get_users_response())

    @validate_schema(user_insert_schema)
    def post(self):
        return make_response(insert_user_response(get_params()))
