from bson.objectid import ObjectId

from jap_dev.queries.word.main import delete_word


def delete_word_response(params):
    word_id = params['word_id']
    if not ObjectId.is_valid(word_id):
        return {'error': 'Invalid ID'}, 400
    query = delete_word(word_id)
    if query.deleted_count > 0:
        return {'id': word_id}, 200
    return {'error': 'Word not found'}, 404
