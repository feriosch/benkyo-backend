def format_summarized_clause(clause):
    formatted_clause = dict()

    formatted_clause['id'] = str(clause['_id'])
    formatted_clause['title'] = clause['title']
    if 'hiragana' in clause:
        formatted_clause['hiragana'] = clause['hiragana']
    formatted_clause['translation'] = clause['translation']
    formatted_clause['level'] = clause['level']

    return formatted_clause


def format_all_clauses(clauses):
    result = []
    for clause in clauses:
        result.append(format_summarized_clause(clause))
    return result
