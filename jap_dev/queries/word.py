from bson.objectid import ObjectId

from jap_dev.information import words


def get_all():
    return words().find()


def get_words_from(collection):
    return words().find({'from': collection})


def check_if_exists(word):
    return words().find({'word': word}).count() > 0


def insert(word):
    inserted_word = words().insert_one(word)
    return inserted_word.inserted_id


def search_one(word):
    return words().find({'word': word})


def search_many(word):
    return words().find({
        '$or': [
            {'word': {'$regex': '^' + word}},
            {'hiragana': {'$regex': '^' + word}},
            {'spanish': {'$regex': '^' + word}}
        ]
    })


def update_word(word_id, info):
    word = words().find_one({'_id': ObjectId(word_id)})
    if word:
        words().update_one({'_id': ObjectId(word_id)}, {'$set': info})
        return True
    return False


def update_word_level(word_id, success):
    word = words().find_one({'_id': ObjectId(word_id)})
    if word:
        if success and word['level'] < 5:
            words().update_one({'_id': ObjectId(word_id)}, {'$inc': {'level': 1}})
            return True
        if not success and word['level'] > 0:
            words().update_one({'_id': ObjectId(word_id)}, {'$inc': {'level': -1}})
            return True
        return False
    return False
