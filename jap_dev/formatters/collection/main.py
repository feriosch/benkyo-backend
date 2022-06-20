def format_collection(collection):
    return {
        'id': str(collection['_id']),
        'printing_name': collection['printing_name'],
        'collection_name': collection['collection_name'],
        'group': collection['group'],
        'image_url': collection['image_url']
    }


def format_all_collections(collections):
    result = []
    for collection in collections:
        result.append(format_collection(collection))
    return result
