from jap_dev.information import clauses


def check_if_clause_exists(title):
    return clauses().count_documents({'title': title}) > 0
