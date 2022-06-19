from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses import group_collection


class MainCollectionView(MethodView):
    decorators = [validate_schema('group_collections_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(group_collection.get_response(params))

    def post(self, body):
        validate_session(request)
        return make_response(group_collection.create_response(body))
