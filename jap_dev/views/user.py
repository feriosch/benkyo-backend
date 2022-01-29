from flask import make_response, request
from flask.views import MethodView

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import user


class User(MethodView):
    decorators = [validate_schema('user_schema')]

    def get(self, _params):
        return make_response(user.get_response())

    def post(self, body):
        return make_response(user.create_response(body))


class Login(MethodView):
    decorators = [validate_schema('login_schema')]

    def post(self, body):
        return make_response(user.login_response(body))


class Session(MethodView):

    def get(self):
        validate_session(request)
        return make_response({'message': 'Valid session'}, 200)
