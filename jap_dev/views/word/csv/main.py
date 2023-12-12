from flask.views import MethodView
from flask import send_from_directory

from jap_dev.helpers.authentication import validate_session
from jap_dev.schemas.validation import validate_schema, get_params
from jap_dev.schemas.word.csv import word_csv_get_schema
import jap_dev.responses.word.csv as responses


class WordCsvMainView(MethodView):
    decorators = [validate_session]

    @validate_schema(word_csv_get_schema)
    def get(self):
        csv_response = responses.get_words_csv_response(get_params())
        if csv_response:
            return send_from_directory('files', f'{csv_response}.csv', as_attachment=True)
        else:
            return {'error': 'Error processing CSV file.'}, 500
