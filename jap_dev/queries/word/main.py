from bson.objectid import ObjectId

from jap_dev.information import words


def get_words(collection, tags, filter_by, order_field, order_direction, page_size, page_number):
    pipeline = []
    if collection:
        pipeline.append({'$match': {'group': collection}})
    if tags:
        tag_conditions = []
        for tag in tags:
            tag_conditions.append({'tags.{}'.format(tag): {'$exists': True}})
        pipeline.append({'$match': {'$and': tag_conditions}})
    if filter_by:
        pipeline.append({
            '$match': {
                '$or': [
                    {'word': {'$regex': filter_by}},
                    {'hiragana': {'$regex': '^' + filter_by}},
                    {'spanish': {
                        '$regex': filter_by,
                        '$options': 'i'
                    }}
                ]
            }
        })
    word_count = get_total_words(pipeline)
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


def get_total_words(main_pipeline):
    pipeline = main_pipeline.copy()
    pipeline.append({'$count': 'total'})
    result = words().aggregate(pipeline)
    if result.alive:
        return result.next().get('total')
    else:
        return 0


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
