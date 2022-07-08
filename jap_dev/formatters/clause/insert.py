def format_type_insertion(clause_type):
    return {
        'adjective': bool(clause_type['adjective']) if ('adjective' in clause_type) else False,
        'adverb': bool(clause_type['adverb']) if ('adverb' in clause_type) else False,
        'auxiliary': bool(clause_type['auxiliary']) if ('auxiliary' in clause_type) else False,
        'conjunction': bool(clause_type['conjunction']) if ('conjunction' in clause_type) else False,
        'modifier': bool(clause_type['modifier']) if ('modifier' in clause_type) else False,
        'noun': bool(clause_type['noun']) if ('noun' in clause_type) else False,
        'particle': bool(clause_type['particle']) if ('particle' in clause_type) else False,
        'phrase': bool(clause_type['phrase']) if ('phrase' in clause_type) else False,
        'structure': bool(clause_type['structure']) if ('structure' in clause_type) else False,
        'suffix': bool(clause_type['suffix']) if ('suffix' in clause_type) else False
    }


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
