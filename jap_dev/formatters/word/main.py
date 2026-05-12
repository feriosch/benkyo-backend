def format_word(word, related_words=None):
    """
    Format a word document for API response.
    
    Args:
        word: The word document from MongoDB
        related_words: Optional dict mapping ObjectId strings to word documents
                      for populating related word details
    """
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
    
    # Format related words if present
    if 'related' in word and word['related']:
        formatted_related = []
        for rel in word['related']:
            if 'wordId' in rel:
                rel_entry = {
                    'wordId': str(rel['wordId']),
                    'type': rel.get('type', 'related'),
                    'note': rel.get('note', ''),
                    'tags': rel.get('tags', [])
                }
                if related_words and str(rel['wordId']) in related_words:
                    related_doc = related_words[str(rel['wordId'])]
                    rel_entry['word'] = related_doc.get('word', '')
                    rel_entry['hiragana'] = related_doc.get('hiragana', '')
                    rel_entry['spanish'] = related_doc.get('spanish', '')
            else:
                rel_entry = {
                    'word': rel.get('word', ''),
                    'type': rel.get('type', 'related'),
                    'note': rel.get('note', ''),
                    'tags': rel.get('tags', []),
                    'isBasic': True
                }
            formatted_related.append(rel_entry)
        formatted_word['related'] = formatted_related
    
    return formatted_word


def format_summarized_word(word):
    formatted_word = dict()

    formatted_word['id'] = str(word['_id'])
    formatted_word['word'] = word['word']
    if 'hiragana' in word:
        formatted_word['hiragana'] = word['hiragana']
    formatted_word['spanish'] = word['spanish']
    if 'tags' in word:
        formatted_word['tags'] = word['tags']
    return formatted_word


def format_all_words(words):
    result = []
    for word in words:
        result.append(format_summarized_word(word))
    return result
