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
    formatted_object = {
        'title': clause_info['title'],
        'translation': clause_info['translation'],
        'level': clause_info['level'],
        'type': format_type_insertion(clause_info['clause_type']),
        'keys': clause_info['keys'],
        'formations': clause_info['formations'],
        'examples': clause_info['examples'],
        'notes': clause_info['notes'],
        'related': clause_info['related']
    }
    if 'tags' in clause_info:
        if clause_info['tags']:
            formatted_object['tags'] = clause_info['tags']
    if 'hiragana' in clause_info:
        formatted_object['hiragana'] = clause_info['hiragana']
    return formatted_object
