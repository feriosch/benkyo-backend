from jap_dev.queries.kanji.radicals import get_distinct_radicals


def get_distinct_radicals_response(params):
    next_page_number = None
    total_pages = 1

    if 'prefix' in params:
        prefix = params['prefix']
        radicals = list(filter(lambda x: x.startswith(prefix), get_distinct_radicals()))
    else:
        radicals = list(get_distinct_radicals())

    total_radicals = len(radicals)

    if 'page_size' in params:
        page_size = int(params['page_size'])
        pages = [radicals[i:i + page_size] for i in range(0, total_radicals, page_size)]
        total_pages = len(pages)
        if 'page_number' in params:
            page_number = int(params['page_number'])
            if page_number < 1 or page_number > total_pages:
                return {'error': 'Page size out of boundaries'}, 400
        else:
            page_number = 1
        if page_number < total_pages:
            next_page_number = page_number + 1
        if pages:
            radicals = pages[page_number - 1]

    return {
        'radicals': radicals,
        'next_page_number': next_page_number,
        'total_pages': total_pages,
        'total_radicals': total_radicals
    }
