from bson.objectid import ObjectId

from jap_dev.information import kanjis


def get_kanji(components, radicalize, filter_by, order_field, order_direction, page_size, page_number):
    pipeline = []
    if components:
        if radicalize:
            pipeline.append({
                '$match': {'radicals': {'$all': components}},
            })
        else:
            pipeline.append({
                '$match': {'components': {'$all': components}}
            })
    if filter_by:
        pipeline.append({
            '$match': {
                '$or': [
                    {'kanji': {'$regex': '^' + filter_by}},
                    {'on': {'$regex': '^' + filter_by}},
                    {'kun': {'$regex': '^' + filter_by}},
                    {'spanish': {
                        '$regex': filter_by,
                        '$options': 'i'
                    }}
                ]
            }
        })
    if order_field:
        pipeline.append({'$sort': {order_field: order_direction}})
    kanji_count = len(list(kanjis().aggregate(pipeline)))
    if page_size:
        skips = page_size * (page_number - 1)
        pipeline.append({'$skip': skips})
        pipeline.append({'$limit': page_size})
    return kanjis().aggregate(pipeline), kanji_count


def insert_kanji(kanji_info):
    inserted_kanji = kanjis().insert_one(kanji_info)
    return inserted_kanji.inserted_id


def update_kanji(kanji_id, info):
    kanji = kanjis().find_one({'_id': ObjectId(kanji_id)})
    if kanji:
        kanjis().update_one({'_id': ObjectId(kanji_id)}, {'$set': info})
        return True
    return False


def update_kanji_deleting_fields(kanji_id, deleted_fields, info):
    kanji = kanjis().find_one({'_id': ObjectId(kanji_id)})
    if kanji:
        kanjis().update_one(
            {'_id': ObjectId(kanji_id)},
            [
                {'$unset': deleted_fields},
                {'$set': info},
            ],
        )
        return True
    return False
