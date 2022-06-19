from flask import make_response, request
from flask.views import MethodView

from jap_dev.helpers.authentication import validate_session


class UserSessionView(MethodView):

    def get(self):
        validate_session(request)
        return make_response({'message': 'Valid session'}, 200)
