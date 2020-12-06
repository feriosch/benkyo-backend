def _format_one(collection):
    return {
        'id': str(collection['_id']),
        'printing_name': collection['printing_name'],
        'collection_name': collection['collection_name'],
        'group': collection['group']
    }


def format_all(collections):
    result = []
    for collection in collections:
        result.append(_format_one(collection))
    return result


def format_insertion(collection_info):
    return {
        'collection_name': collection_info['collection_name'],
        'printing_name': collection_info['printing_name'],
        'group': collection_info['group']
    }
