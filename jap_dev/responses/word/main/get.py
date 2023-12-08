import math

from jap_dev.queries.word.main import get_words
from jap_dev.formatters.word.main import format_all_words


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


def get_words_response(params):
    collection = None
    tags = []
    filter_by = None
    order_field = None
    order_direction = None
    page_size = None
    page_number = None

    if 'group' in params and params['group'] != 'all':
        collection = params['group']
    if 'tag_1' in params:
        tags.append(params['tag_1'])
    if 'tag_2' in params:
        tags.append(params['tag_2'])
    if 'tag_3' in params:
        tags.append(params['tag_3'])
    if 'filter_by' in params:
        filter_by = params['filter_by']
    if 'order_field' in params:
        order_field = params['order_field']
        if 'order_direction' in params:
            if params['order_direction'] == 'ASC':
                order_direction = 1
            elif params['order_direction'] == 'DESC':
                order_direction = -1
            else:
                return {'error': 'Order field must be ASC or DESC'}, 400
        else:
            order_direction = 1
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

    words, word_count = get_words(
        collection=collection,
        tags=tags,
        filter_by=filter_by,
        order_field=order_field,
        order_direction=order_direction,
        page_size=page_size,
        page_number=page_number
    )
    formatted_words = format_all_words(words)
    page_count, next_page_number = get_pagination_details(
        word_count,
        len(formatted_words),
        page_size,
        page_number
    )

    return {
        'words': formatted_words,
        'next_page_number': next_page_number,
        'total_pages': page_count,
        'total_words': word_count
    }
