def format_type_insertion(clause_type):
    formatted_type = dict()

    if 'adjective' in clause_type and clause_type['adjective']:
        formatted_type['adjective'] = True
    if 'adverb' in clause_type and clause_type['adverb']:
        formatted_type['adverb'] = True
    if 'auxiliary' in clause_type and clause_type['auxiliary']:
        formatted_type['auxiliary'] = True
    if 'conjunction' in clause_type and clause_type['conjunction']:
        formatted_type['conjunction'] = True
    if 'modifier' in clause_type and clause_type['modifier']:
        formatted_type['modifier'] = True
    if 'noun' in clause_type and clause_type['noun']:
        formatted_type['noun'] = True
    if 'particle' in clause_type and clause_type['particle']:
        formatted_type['particle'] = True
    if 'phrase' in clause_type and clause_type['phrase']:
        formatted_type['phrase'] = True
    if 'structure' in clause_type and clause_type['structure']:
        formatted_type['structure'] = True
    if 'suffix' in clause_type and clause_type['suffix']:
        formatted_type['suffix'] = True

    return formatted_type


def format_clause_insertion(clause_info):
    formatted_object = dict()

    formatted_object['title'] = clause_info['title']
    if 'hiragana' in clause_info:
        formatted_object['hiragana'] = clause_info['hiragana']
    formatted_object['translation'] = clause_info['translation']
    formatted_object['level'] = clause_info['level']
    formatted_object['type'] = format_type_insertion(clause_info['clause_type'])
    if 'tags' in clause_info:
        if clause_info['tags']:
            formatted_object['tags'] = clause_info['tags']
    formatted_object['definition'] = clause_info['definition']
    formatted_object['keys'] = clause_info['keys']
    formatted_object['formations'] = clause_info['formations']
    if 'examples' in clause_info:
        formatted_object['examples'] = clause_info['examples']
    formatted_object['notes'] = clause_info['notes']
    if 'related' in clause_info:
        formatted_object['related'] = clause_info['related']

    return formatted_object
