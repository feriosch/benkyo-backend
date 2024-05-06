import copy

from jap_dev.information import group_collections


def get_collections(group, search_filter, page_size, page_number):
    pipeline = []
    if group:
        pipeline.append({'$match': {'group': group}})
    if search_filter:
        pipeline.append({
            '$match': {
                '$or': [
                    {'printing_name': {'$regex': '^' + search_filter}},
                    {'collection_name': {'$regex': '^' + search_filter}},
                ]
            }
        })
    collection_count = get_total_collections(pipeline)
    pipeline.append({
        '$sort': {
            'group': 1,
            'collection_name': 1
        }
    })
    if page_size:
        skips = page_size * (page_number - 1)
        pipeline.append({'$skip': skips})
        pipeline.append({'$limit': page_size})
    return group_collections().aggregate(pipeline), collection_count


def get_total_collections(pipeline):
    count_pipeline = copy.deepcopy(pipeline)
    count_pipeline.append({'$count': 'total'})
    cursor = group_collections().aggregate(count_pipeline)
    if cursor.alive:
        return group_collections().aggregate(count_pipeline).next().get('total')
    return 0


def insert_collection(collection):
    inserted_collection = group_collections().insert_one(collection)
    return inserted_collection.inserted_id
