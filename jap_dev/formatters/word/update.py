from jap_dev.formatters.word.insert import format_type_insertion


def format_word_update(word_info):
    formatted_info = dict()
    if 'group' in word_info:
        formatted_info['group'] = word_info['group']
    if 'spanish' in word_info:
        formatted_info['spanish'] = word_info['spanish']
    if 'hiragana' in word_info:
        formatted_info['hiragana'] = word_info['hiragana']
    if 'word_type' in word_info:
        formatted_info['type'] = format_type_insertion(word_info['word_type'])
    if 'tags' in word_info:
        formatted_info['tags'] = word_info['tags']
    if 'sentences' in word_info:
        formatted_info['sentences'] = word_info['sentences']
    if 'notes' in word_info:
        formatted_info['notes'] = word_info['notes']
    return formatted_info
