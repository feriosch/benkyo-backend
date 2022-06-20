from bson.objectid import ObjectId

from jap_dev.information import words


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
