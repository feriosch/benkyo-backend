from bson.objectid import ObjectId

from jap_dev.information import clauses


def get_one_by_id(clause_id):
    return clauses().find_one({'_id': ObjectId(clause_id)})


def get_one_by_title(title):
    return clauses().find_one({'title': title})
