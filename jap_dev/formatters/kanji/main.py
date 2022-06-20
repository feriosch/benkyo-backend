def format_kanji(kanji):
    v2 = None
    on = None
    kun = None
    components = None
    story = None
    recursive = False
    if 'v2' in kanji:
        v2 = int(kanji['v2'])
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
        'v2': v2,
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
        result.append(format_kanji(kanji))
    return result
