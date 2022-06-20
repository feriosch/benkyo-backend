from flask.views import MethodView
from flask import request, make_response

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
from jap_dev.responses.collection.main.get import get_collections_response
from jap_dev.responses.collection.main.insert import insert_collection_response


class MainCollectionView(MethodView):
    decorators = [validate_schema('group_collections_schema')]

    def get(self, params):
        validate_session(request)
        return make_response(get_collections_response(params))

    def post(self, body):
        validate_session(request)
        return make_response(insert_collection_response(body))
