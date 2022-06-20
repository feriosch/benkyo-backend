from bson.objectid import ObjectId

from jap_dev.information import words


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


def insert_word(word):
    inserted_word = words().insert_one(word)
    return inserted_word.inserted_id


def update_word(word_id, info):
    word = words().find_one({'_id': ObjectId(word_id)})
    if word:
        words().update_one({'_id': ObjectId(word_id)}, {'$set': info})
        return True
    return False


def delete_word(word_id):
    return words().delete_one({'_id': ObjectId(word_id)})
