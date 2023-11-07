def format_type_insertion(word_type):
    return {
        'noun': int(word_type['noun']) if ('noun' in word_type) else 0,
        'suru_verb': int(word_type['suru_verb']) if ('suru_verb' in word_type) else 0,
        'no_adjective': int(word_type['no_adjective']) if ('no_adjective' in word_type) else 0,
        'na_adjective': int(word_type['na_adjective']) if ('na_adjective' in word_type) else 0,
        'i_adjective': int(word_type['i_adjective']) if ('i_adjective' in word_type) else 0,
        'adverb': int(word_type['adverb']) if ('adverb' in word_type) else 0,
        'verb': int(word_type['verb']) if ('verb' in word_type) else 0,
        'adjectival_noun': int(word_type['adjectival_noun']) if ('adjectival_noun' in word_type) else 0,
        'adverbial_noun': int(word_type['adverbial_noun']) if ('adverbial_noun' in word_type) else 0,
        'counter': int(word_type['counter']) if ('counter' in word_type) else 0
    }


def format_word_insertion(word_info):
    formatted_object = {
        'word': word_info['word'],
        'spanish': word_info['spanish'],
        'group': word_info['group'],
        'level': int(word_info['level']) if ('level' in word_info) else 0,
        'sentences': word_info['sentences'] if ('sentences' in word_info) else [],
        'type': format_type_insertion(word_info['word_type'])
        if ('word_type' in word_info) else format_type_insertion({}),
    }
    if 'tags' in word_info:
        if word_info['tags']:
            formatted_object['tags'] = word_info['tags']
    if 'hiragana' in word_info:
        formatted_object['hiragana'] = word_info['hiragana']
    if 'notes' in word_info:
        formatted_object['notes'] = word_info['notes']
    return formatted_object
