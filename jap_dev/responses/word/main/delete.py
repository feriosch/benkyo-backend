from bson.objectid import ObjectId

from jap_dev.queries import word as queries


def delete_word_response(params):
    word_id = params['word_id']
    if not ObjectId.is_valid(word_id):
        return {'error': 'Invalid ID'}, 400
    query = queries.delete_word(word_id)
    if query.deleted_count > 0:
        return {'id': word_id}, 200
    return {'error': 'Word not found'}, 404
