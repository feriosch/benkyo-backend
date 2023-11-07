from bson.objectid import ObjectId

from jap_dev.queries.word.verify import check_if_collection_exists
from jap_dev.queries.word.main import update_word
from jap_dev.formatters.word.update import format_word_update


def update_word_response(params):
    word_id = params['word_id']
    if not ObjectId.is_valid(word_id):
        return {'error': 'Invalid ID'}, 400
    if 'group' in params:
        # TODO: Check this out
        if not check_if_collection_exists(params['group']):
            return {'error': 'Collection not found'}, 404
    formatted_word = format_word_update(params)
    if update_word(word_id, formatted_word):
        return {'id': word_id}, 200
    return {'error': 'No matched word'}, 400
