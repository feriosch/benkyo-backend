from flask.views import MethodView
from flask import send_from_directory

from jap_dev.helpers.authentication import validate_session
from jap_dev.responses.kanji.csv import get_kanjis_csv_response


class KanjiCsvView(MethodView):
    decorators = [validate_session]

    def get(self):
        csv_response = get_kanjis_csv_response()
        if csv_response:
            return send_from_directory('files', 'kanji.csv', as_attachment=True)
        return {'error': 'Error processing CSV file.'}, 500
