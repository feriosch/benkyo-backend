def format_kanji_insertion(kanji_info):
    formatted_info = {
        'v1': kanji_info['v1'],
        'kanji': kanji_info['kanji'],
        'spanish': kanji_info['spanish'],
    }
    if 'v2' in kanji_info:
        formatted_info['v2'] = kanji_info['v2']
    if 'on' in kanji_info:
        formatted_info['on'] = kanji_info['on']
    if 'kun' in kanji_info:
        formatted_info['kun'] = kanji_info['kun']
    if 'components' in kanji_info and len(kanji_info['components']) > 0:
        formatted_info['components'] = kanji_info['components']
        if kanji_info['spanish'] in set(kanji_info['components']):
            formatted_info['recursive'] = True
    if 'story' in kanji_info:
        formatted_info['story'] = kanji_info['story']
    return formatted_info
