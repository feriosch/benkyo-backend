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


def search_one_by_word(word):
    return words().find_one({'word': word})


def search_one_by_id(word_id):
    return words().find_one({'_id': ObjectId(word_id)})


def search_one_random_by_collection(collection):
    return words().aggregate([
        {'$match': {'from': collection}},
        {'$sample': {'size': 1}}
    ])


def search_one_random():
    return words().aggregate([
        {'$sample': {'size': 1}}
    ])


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
        return True
    return False


def get_words_for_csv(collection=None):
    if collection:
        return words().find({'from': collection}, {'_id': 0, 'word': 1, 'hiragana': 1, 'spanish': 1})
    else:
        return words().find({}, {'_id': 0, 'word': 1, 'hiragana': 1, 'spanish': 1})
