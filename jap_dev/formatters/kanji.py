def _format_kanji(kanji):
    on = None
    kun = None
    components = None
    story = None
    recursive = False
    if 'on' in kanji:
        on = kanji['on']
    if 'kun' in kanji:
        kun = kanji['kun']
    if 'components' in kanji:
        components = kanji['components']
    if 'story' in kanji:
        story = kanji['story']
    if 'recursive' in kanji:
        recursive = True
    return {
        'id': str(kanji['_id']),
        'v1': int(kanji['v1']),
        'v2': int(kanji['v2']),
        'kanji': kanji['kanji'],
        'on': on,
        'kun': kun,
        'spanish': kanji['spanish'],
        'components': components,
        'radicals': kanji['radicals'],
        'story': story,
        'recursive': recursive
    }


def format_all_kanjis(kanjis):
    result = []
    for kanji in kanjis:
        result.append(_format_kanji(kanji))
    return result


def format_kanji_insertion(kanji_info):
    formatted_object = {
        'v1': kanji_info['v1'],
        'kanji': kanji_info['kanji'],
        'spanish': kanji_info['spanish'],
    }
    if 'v2' in kanji_info:
        formatted_object['v2'] = kanji_info['v2']
    if 'on' in kanji_info:
        formatted_object['on'] = kanji_info['on']
    if 'kun' in kanji_info:
        formatted_object['kun'] = kanji_info['kun']
    if 'components' in kanji_info and len(kanji_info['components']) > 0:
        formatted_object['components'] = kanji_info['components']
        if kanji_info['spanish'] in set(kanji_info['components']):
            formatted_object['recursive'] = True
    if 'story' in kanji_info:
        formatted_object['story'] = kanji_info['story']
    return formatted_object
