from flask.views import MethodView
from flask import send_from_directory

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.word.csv import word_csv_get_schema
import jap_dev.responses.word.csv as responses


class WordCsvView(MethodView):
    decorators = [validate_session]

    # Todo: Evaluate if refactor to a response
    @validate_schema(word_csv_get_schema)
    def get(self):
        params = get_params()
        if 'group' in params:
            collection = params['group']
            csv_response = responses.get_words_csv_response(collection)
            if csv_response:
                return send_from_directory('files', f'{collection}.csv', as_attachment=True)
            else:
                return {'error': 'Error processing CSV file.'}, 500
        else:
            csv_response = responses.get_words_csv_response(None)
            if csv_response:
                return send_from_directory('files', 'benkyo.csv', as_attachment=True)
            return {'error': 'Error processing CSV file.'}, 500
