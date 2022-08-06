def format_full_clause(clause):
    formatted_clause = dict()

    formatted_clause['id'] = str(clause['_id'])
    formatted_clause['title'] = clause['title']

    if 'hiragana' in clause:
        formatted_clause['hiragana'] = clause['hiragana']
    formatted_clause['translation'] = clause['translation']

    formatted_clause['level'] = clause['level']
    formatted_clause['type'] = clause['type']

    if 'tags' in clause:
        formatted_clause['tags'] = clause['tags']
    formatted_clause['definition'] = clause['definition']

    formatted_keys = clause['keys']
    for key in formatted_keys:
        key['sentence'] = format_sentence(key['sentence'])
    formatted_clause['keys'] = formatted_keys

    formatted_formations = clause['formations']
    for formation in formatted_formations:
        examples = formation['examples']
        for example in examples:
            example['sentence'] = format_sentence(example['sentence'])
    formatted_clause['formations'] = formatted_formations

    if 'examples' in clause:
        formatted_examples = clause['examples']
        for example in formatted_examples:
            example['sentence'] = format_sentence(example['sentence'])
        formatted_clause['examples'] = formatted_examples

    formatted_notes = clause['notes']
    for note in formatted_notes:
        if 'examples' in note:
            examples = note['examples']
            for example in examples:
                example['sentence'] = format_sentence(example['sentence'])
    formatted_clause['notes'] = formatted_notes

    if 'related' in clause:
        formatted_related = clause['related']
        for related_element in formatted_related:
            sections = related_element['sections']
            for section in sections:
                if 'examples' in section:
                    examples = section['examples']
                    for example in examples:
                        example['sentence'] = format_sentence(example['sentence'])
        formatted_clause['related'] = formatted_related

    return formatted_clause


def format_sentence(sentence):
    symbols = ['*', '_', '$']
    sentence_components = list()
    is_between_symbols = False
    component = str()

    for character in sentence:
        if character in symbols:
            if is_between_symbols is False:
                if component:
                    sentence_components.append(component)
                component = str()
                component += character
                component += '|'
                is_between_symbols = True
            else:
                sentence_components.append(component)
                is_between_symbols = False
                component = str()
        else:
            component += character
            if sentence.index(character) == (len(sentence) - 1):
                sentence_components.append(component)

    return sentence_components
