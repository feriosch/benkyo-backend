import math

from jap_dev.queries.clause.main import get_clauses
from jap_dev.formatters.clause.main import format_all_clauses


def get_pagination_details(total_clause_count, result_size, page_size, page_number):
    total_page_count = 1
    if not page_size:
        return total_page_count, ''
    skips = page_size * (page_number - 1)
    total_page_count = math.ceil(total_clause_count / page_size)
    if skips + result_size < total_clause_count:
        return total_page_count, str(page_number + 1)
    else:
        return total_page_count, ''


def get_clauses_response(params):
    level = None
    filter_by = None
    order_field = None
    order_direction = None
    page_size = None
    page_number = None

    if 'level' in params:
        level = params['level']
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

    clauses, clause_count = get_clauses(
        level=level,
        filter_by=filter_by,
        order_field=order_field,
        order_direction=order_direction,
        page_size=page_size,
        page_number=page_number
    )

    formatted_clauses = format_all_clauses(clauses)
    page_count, next_page_number = get_pagination_details(
        clause_count,
        len(formatted_clauses),
        page_size,
        page_number
    )

    return {
        'clauses': formatted_clauses,
        'next_page_number': next_page_number,
        'total_pages': page_count,
        'total_clauses': clause_count
    }
