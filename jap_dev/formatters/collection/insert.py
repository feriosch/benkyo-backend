def format_collection_insertion(collection_info, image_url):
    return {
        'collection_name': collection_info['collection_name'],
        'printing_name': collection_info['printing_name'],
        'group': collection_info['group'],
        'image_url': image_url
    }
