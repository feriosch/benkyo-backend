from flask.views import MethodView
from flask import make_response

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.collection.search import search_collection_schema
import jap_dev.responses.collection.search as responses


class CollectionSearchView(MethodView):
    decorators = [validate_session]

    @validate_schema(search_collection_schema)
    def get(self):
        params = get_params()
        return make_response(responses.get_one_collection_by_name_response(params['name']))
