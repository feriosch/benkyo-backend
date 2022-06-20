from flask.views import MethodView
from flask import request, send_from_directory

from jap_dev.helpers.validation import validate_schema
from jap_dev.helpers.authentication import validate_session
import jap_dev.responses.word.csv as responses


class WordCsvView(MethodView):
    decorators = [validate_schema('word_csv_schema')]

    def get(self, params):
        validate_session(request)
        if 'from' in params:
            collection = params['from']
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
