from flask.views import MethodView
from flask import (make_response)

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import authenticate_jwt
from jap_dev.responses import group_collection


class GroupCollection (MethodView):
    decorators = [authenticate_jwt(), validate_schema('group_collections_schema')]

    def get(self, _params):
        return make_response(group_collection.get_response())

    def post(self, body):
        return make_response(group_collection.create_response(body))
