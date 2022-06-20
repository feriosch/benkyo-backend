from bson.objectid import ObjectId

from jap_dev.information import words


def update_word_level(word_id, success):
    word = words().find_one({'_id': ObjectId(word_id)})
    if word:
        if success and word['level'] < 5:
            words().update_one({'_id': ObjectId(word_id)}, {'$inc': {'level': 1}})
            return True
        if not success and word['level'] > 0:
            words().update_one({'_id': ObjectId(word_id)}, {'$inc': {'level': -1}})
            return True
        return True
    return False
