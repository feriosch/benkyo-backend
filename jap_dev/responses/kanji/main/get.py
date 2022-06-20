import math

from jap_dev.queries.kanji.main import get_kanji
from jap_dev.formatters.kanji.summarized import format_all_summarized_kanjis


def get_pagination_details(total_kanji_count, result_size, page_size, page_number):
    total_page_count = 1
    if not page_size:
        return total_page_count, ''
    skips = page_size * (page_number - 1)
    total_page_count = math.ceil(total_kanji_count / page_size)
    if skips + result_size < total_kanji_count:
        return total_page_count, str(page_number + 1)
    else:
        return total_page_count, ''


def get_kanji_response(params):
    filter_by = None
    order_field = None
    order_direction = None
    page_size = None
    page_number = None
    components = []
    if 'c1' in params:
        components.append(params['c1'])
    if 'c2' in params:
        components.append(params['c2'])
    if 'c3' in params:
        components.append(params['c3'])
    if 'c4' in params:
        components.append(params['c4'])
    if 'c5' in params:
        components.append(params['c5'])
    if 'c6' in params:
        components.append(params['c6'])
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

    kanjis, kanji_count = get_kanji(
        components=components,
        filter_by=filter_by,
        order_field=order_field,
        order_direction=order_direction,
        page_size=page_size,
        page_number=page_number
    )
    formatted_kanjis = format_all_summarized_kanjis(kanjis)
    page_count, next_page_number = get_pagination_details(
        kanji_count,
        len(formatted_kanjis),
        page_size,
        page_number
    )

    return {
        'kanjis': formatted_kanjis,
        'next_page_number': next_page_number,
        'total_pages': page_count,
        'total_kanjis': kanji_count
    }
