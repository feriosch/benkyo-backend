def format_type_insertion(word_type):
    word_formatted_type = dict()
    if 'noun' in word_type:
        word_formatted_type['noun'] = int(word_type['noun'])
    if 'suru' in word_type:
        word_formatted_type['suru'] = int(word_type['suru'])
    if 'no_adj' in word_type:
        word_formatted_type['no_adj'] = int(word_type['no_adj'])
    if 'na_adj' in word_type:
        word_formatted_type['na_adj'] = int(word_type['na_adj'])
    if 'i_adj' in word_type:
        word_formatted_type['i_adj'] = int(word_type['i_adj'])
    if 'adv' in word_type:
        word_formatted_type['adv'] = int(word_type['adv'])
    if 'verb' in word_type:
        word_formatted_type['verb'] = int(word_type['verb'])
    if 'adj_noun' in word_type:
        word_formatted_type['adj_noun'] = int(word_type['adj_noun'])
    if 'adv_noun' in word_type:
        word_formatted_type['adv_noun'] = int(word_type['adv_noun'])
    if 'counter' in word_type:
        word_formatted_type['counter'] = int(word_type['counter'])
    return word_formatted_type


def format_word_insertion(word_info):
    formatted_object = {
        'word': word_info['word'],
        'spanish': word_info['spanish'],
        'group': word_info['group'],
        'sentences': word_info['sentences'] if ('sentences' in word_info) else [],
        'type': format_type_insertion(word_info['word_type'])
    }
    if 'tags' in word_info:
        if word_info['tags']:
            formatted_object['tags'] = word_info['tags']
    if 'hiragana' in word_info:
        formatted_object['hiragana'] = word_info['hiragana']
    if 'notes' in word_info:
        formatted_object['notes'] = word_info['notes']
    return formatted_object
