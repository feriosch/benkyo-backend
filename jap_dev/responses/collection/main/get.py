import math

from jap_dev.queries.collection.main import get_collections
from jap_dev.formatters.collection.main import format_all_collections


def get_pagination_details(total_collection_count, result_size, page_size, page_number):
    total_page_count = 1
    if not page_size:
        return total_page_count, ''
    skips = page_size * (page_number - 1)
    total_page_count = math.ceil(total_collection_count / page_size)
    if skips + result_size < total_collection_count:
        return total_page_count, str(page_number + 1)
    else:
        return total_page_count, ''


def get_collections_response(params):
    group = None
    search_filter = None
    page_size = None
    page_number = None

    if 'group' in params:
        group = params['group']
    if 'filter' in params:
        search_filter = params['filter']
    if 'page_size' in params:
        page_size = int(params['page_size'])
        if page_size < 1 or page_size > 1000:
            return {'error': 'Page size out of boundaries'}, 400
        if 'page_number' in params:
            page_number = int(params['page_number'])
            if page_number < 1:
                return {'error': 'Page number out of boundaries'}, 400
        else:
            page_number = 1

    collections, collection_count = get_collections(
        group=group,
        search_filter=search_filter,
        page_size=page_size,
        page_number=page_number
    )
    formatted_collections = format_all_collections(collections)
    page_count, next_page_number = get_pagination_details(
        collection_count,
        len(formatted_collections),
        page_size,
        page_number
    )

    return {
        'collections': formatted_collections,
        'next_page_number': next_page_number,
        'total_pages': page_count,
        'total_collections': collection_count
    }
