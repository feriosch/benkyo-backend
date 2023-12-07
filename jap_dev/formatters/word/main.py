def format_word(word):
    formatted_word = {
        'id': str(word['_id']),
        'word': word['word'],
        'spanish': word['spanish'],
        'group': word['group'],
        'sentences': word['sentences'],
        'type': word['type']
    }
    if 'hiragana' in word:
        formatted_word['hiragana'] = word['hiragana']
    if 'tags' in word:
        formatted_word['tags'] = word['tags']
    if 'notes' in word:
        formatted_word['notes'] = word['notes']
    return formatted_word


def format_summarized_word(word):
    formatted_word = dict()

    formatted_word['id'] = str(word['_id'])
    formatted_word['word'] = word['word']
    if 'hiragana' in word:
        formatted_word['hiragana'] = word['hiragana']
    formatted_word['spanish'] = word['spanish']

    return formatted_word


def format_all_words(words):
    result = []
    for word in words:
        result.append(format_summarized_word(word))
    return result
