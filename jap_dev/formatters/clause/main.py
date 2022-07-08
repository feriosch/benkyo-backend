def format_summarized_clause(clause):
    formatted_clause = {
        'id': str(clause['_id']),
        'title': clause['title'],
        'level': clause['level'],
        'translation': clause['translation']
    }
    if 'hiragana' in clause:
        formatted_clause['hiragana'] = clause['hiragana']
    return formatted_clause


def format_all_clauses(clauses):
    result = []
    for clause in clauses:
        result.append(format_summarized_clause(clause))
    return result
