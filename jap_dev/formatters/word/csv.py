def format_type(word_type):
    formatted_type = []
    japanese_subtypes = {
        'noun': '名',
        'suru': 'する',
        'no_adj': 'の形',
        'na_adj': 'な形',
        'i_adj': 'い形',
        'adv': '副',
        'verb': '動',
        'adj_noun': '名形',
        'adv_noun': '副名',
        'counter': '回'
    }
    for key, value in word_type.items():
        if value == 1 and key in japanese_subtypes:
            formatted_type.append(japanese_subtypes[key])
    return '、'.join(formatted_type)


def format_csv_word(word):
    formatted_word = word
    if 'type' in word:
        formatted_word['type'] = format_type(word['type'])
    if 'tags' in word:
        if 'common' in word['tags']:
            formatted_word['common'] = True
        if 'jlpt_n1' in word['tags']:
            formatted_word['jlpt_n1'] = True
        if 'expression' in word['tags']:
            formatted_word['expression'] = True
        if 'onomatopoeic' in word['tags']:
            formatted_word['onomatopoeic'] = True
    return formatted_word


def format_all_csv_words(words):
    result = []
    for word in words:
        result.append(format_csv_word(word))
    return result
