from flask import (jsonify)
from bson.objectid import ObjectId

import jap_dev.queries.clause.search as queries
from jap_dev.formatters.clause.search import format_full_clause


def get_one_clause_by_id_response(clause_id):
    if not ObjectId.is_valid(clause_id):
        return {'error': 'Invalid ID'}, 400
    result = queries.get_one_by_id(clause_id)
    if result is None:
        return {'error': 'No matched clause'}, 400
    return jsonify(format_full_clause(result))
