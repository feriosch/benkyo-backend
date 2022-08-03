from jap_dev.formatters.clause.insert import format_type_insertion


def format_clause_update(clause_info):
    formatted_clause_info = dict()

    if 'title' in clause_info:
        formatted_clause_info['title'] = clause_info['title']
    
    if 'hiragana' in clause_info:
        formatted_clause_info['hiragana'] = clause_info['hiragana']
    
    if 'translation' in clause_info:
        formatted_clause_info['translation'] = clause_info['translation']
    
    if 'level' in clause_info:
        formatted_clause_info['level'] = clause_info['level']

    if 'clause_type' in clause_info:
        formatted_clause_info['type'] = format_type_insertion(clause_info['clause_type'])

    if 'tags' in clause_info:
        formatted_clause_info['tags'] = clause_info['tags']

    if 'definition' in clause_info:
        formatted_clause_info['definition'] = clause_info['definition']

    if 'keys' in clause_info:
        formatted_clause_info['keys'] = clause_info['keys']

    if 'formations' in clause_info:
        formatted_clause_info['formations'] = clause_info['formations']

    if 'examples' in clause_info:
        formatted_clause_info['examples'] = clause_info['examples']

    if 'notes' in clause_info:
        formatted_clause_info['notes'] = clause_info['notes']

    if 'related' in clause_info:
        formatted_clause_info['related'] = clause_info['related']

    return formatted_clause_info
