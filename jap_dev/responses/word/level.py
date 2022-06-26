from jap_dev.queries.word.level import update_word_level


def update_level_response(word_id, success):
    bool_success = bool(int(success))
    if update_word_level(word_id, bool_success):
        return {'id': word_id}, 200
    return {'error': 'No matched word'}, 400
