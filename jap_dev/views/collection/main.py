from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.collection.main.get import collection_get_schema
from jap_dev.schemas.collection.main.insert import collection_insert_schema
from jap_dev.responses.collection.main.get import get_collections_response
from jap_dev.responses.collection.main.insert import insert_collection_response


class MainCollectionView(MethodView):
    decorators = [validate_session]

    @validate_schema(collection_get_schema)
    def get(self):
        return make_response(get_collections_response(get_params()))

    @validate_schema(collection_insert_schema)
    def post(self):
        return make_response(insert_collection_response(get_params()))
