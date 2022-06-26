from flask import make_response
from flask.views import MethodView

from jap_dev.helpers.authentication import validate_session


class UserSessionView(MethodView):
    decorators = [validate_session]

    def get(self):
        return make_response({'message': 'Valid session'}, 200)
