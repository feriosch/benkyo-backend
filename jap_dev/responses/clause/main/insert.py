from flask import (jsonify)

from jap_dev.queries.clause.verify import check_if_clause_exists
from jap_dev.queries.clause.main import insert_clause
from jap_dev.formatters.clause.insert import format_clause_insertion
from jap_dev.formatters.id.main import format_response_id


def insert_clause_response(clause_info):
    if check_if_clause_exists(clause_info['title']):
        return {'error': 'Clause repeated'}, 400
    formatted_clause = format_clause_insertion(clause_info)
    inserted_id = insert_clause(formatted_clause)
    return jsonify(format_response_id(inserted_id))
