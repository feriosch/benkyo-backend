import math

from bson.objectid import ObjectId

from jap_dev.information import words


def get_all():
    return words().find()


def get_words(collection, filter_by, order_field, order_direction, page_size, page_number):
    pipeline = []
    if collection:
        pipeline.append({'$match': {'from': collection}})
    if filter_by:
        pipeline.append({
            '$match': {
                '$or': [
                    {'word': {'$regex': '^' + filter_by}},
                    {'hiragana': {'$regex': '^' + filter_by}},
                    {'spanish': {
                        '$regex': filter_by,
                        '$options': 'i'
                    }}
                ]
            }
        })
    if order_field:
        pipeline.append({'$sort': {order_field: order_direction}})
    word_count = len(list(words().aggregate(pipeline)))
    if page_size:
        skips = page_size * (page_number - 1)
        pipeline.append({'$skip': skips})
        pipeline.append({'$limit': page_size})
    return words().aggregate(pipeline), word_count


def get_pagination_details(total_word_count, result_size, page_size, page_number):
    total_page_count = 1
    if not page_size:
        return total_page_count, ''
    skips = page_size * (page_number - 1)
    total_page_count = math.ceil(total_word_count / page_size)
    if skips + result_size < total_word_count:
        return total_page_count, str(page_number + 1)
    else:
        return total_page_count, ''


def check_if_word_exists(word):
    return words().count_documents({'word': word}) > 0


def check_if_collection_exists(collection):
    return collection in words().distinct('from')


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


def delete_word(word_id):
    return words().delete_one({'_id': ObjectId(word_id)})


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
