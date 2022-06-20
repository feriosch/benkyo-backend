from jap_dev.queries import word as queries


def update_level_response(word_id, success):
    bool_success = bool(int(success))
    if queries.update_word_level(word_id, bool_success):
        return {'id': word_id}, 200
    return {'error': 'No matched word'}, 400
