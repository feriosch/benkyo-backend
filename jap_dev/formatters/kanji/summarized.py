def format_summarized_kanji(kanji):
    formatted_kanji = {
        'id': str(kanji['_id']),
        'v1': int(kanji['v1']),
        'kanji': kanji['kanji'],
        'spanish': kanji['spanish']
    }
    if 'v2' in kanji:
        formatted_kanji['v2'] = int(kanji['v2'])
    if 'on' in kanji:
        formatted_kanji['on'] = kanji['on']
    if 'kun' in kanji:
        formatted_kanji['kun'] = kanji['kun']
    return formatted_kanji


def format_all_summarized_kanjis(kanjis):
    result = []
    for kanji in kanjis:
        result.append(format_summarized_kanji(kanji))
    return result
