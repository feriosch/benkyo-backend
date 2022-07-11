from bson.objectid import ObjectId

from jap_dev.queries.clause.main import delete_clause


def delete_clause_response(params):
    clause_id = params['clause_id']
    if not ObjectId.is_valid(clause_id):
        return {'error': 'Invalid ID'}, 400
    query = delete_clause(clause_id)
    if query.deleted_count > 0:
        return {'id': clause_id}, 200
    return {'error': 'Clause not found'}, 404
