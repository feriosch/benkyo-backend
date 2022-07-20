from bson.objectid import ObjectId

from jap_dev.information import words


def get_words(collection, filter_by, order_field, order_direction, page_size, page_number):
    pipeline = []
    if collection:
        pipeline.append({'$match': {'from': collection}})
        word_count = get_total_words(collection)
    else:
        word_count = get_total_words()
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
    if page_size:
        skips = page_size * (page_number - 1)
        pipeline.append({'$skip': skips})
        pipeline.append({'$limit': page_size})
    pipeline.append({
        '$project': {
            '_id': 1,
            'word': 1,
            'hiragana': 1,
            'spanish': 1
        }
    })
    return words().aggregate(pipeline), word_count


def get_total_words(collection=None):
    pipeline = []
    if collection:
        pipeline.append({'$match': {'from': collection}})
    pipeline.append({'$count': 'total'})
    return words().aggregate(pipeline).next().get('total')


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
