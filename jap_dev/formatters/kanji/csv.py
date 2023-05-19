def format_csv_kanji(kanji):
    if 'components' in kanji:
        kanji['components'] = ", ".join(kanji['components'])
    return kanji


def format_all_csv_kanjis(kanjis):
    result = []
    for kanji in kanjis:
        result.append(format_csv_kanji(kanji))
    return result
