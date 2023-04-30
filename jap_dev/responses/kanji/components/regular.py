from jap_dev.queries.kanji.components.regular import get_distinct_components


def get_distinct_components_response(params):
    next_page_number = None
    total_pages = 1

    if 'prefix' in params:
        prefix = params['prefix']
        components = list(filter(lambda x: x.startswith(prefix), get_distinct_components()))
    else:
        components = list(get_distinct_components())

    total_components = len(components)

    if 'page_size' in params:
        page_size = int(params['page_size'])
        pages = [components[i:i + page_size] for i in range(0, total_components, page_size)]
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
            components = pages[page_number - 1]

    return {
        'components': components,
        'next_page_number': next_page_number,
        'total_pages': total_pages,
        'total_components': total_components
    }
