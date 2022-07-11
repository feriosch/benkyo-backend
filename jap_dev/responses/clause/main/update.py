from bson.objectid import ObjectId

from jap_dev.queries.clause.main import update_clause
from jap_dev.formatters.clause.update import format_clause_update


def update_clause_response(params):
    clause_id = params['clause_id']
    if not ObjectId.is_valid(clause_id):
        return {'error': 'clause ID error'}, 400
    formatted_clause = format_clause_update(params)
    if update_clause(clause_id, formatted_clause):
        return {'id': clause_id}, 200
    return {'error': 'No matched clause'}, 400
