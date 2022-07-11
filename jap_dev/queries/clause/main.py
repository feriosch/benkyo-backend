from bson.objectid import ObjectId

from jap_dev.information import clauses


def get_clauses(level, filter_by, order_field, order_direction, page_size, page_number):
    pipeline = []
    if level:
        pipeline.append({'$match': {'level': level}})
    if filter_by:
        pipeline.append({
            '$match': {
                '$or': [
                    {'title': {'$regex': '^' + filter_by}},
                    {'hiragana': {'$regex': '^' + filter_by}},
                    {'translation': {
                        '$regex': filter_by,
                        '$options': 'i'
                    }}
                ]
            }
        })
    if order_field:
        pipeline.append({'$sort': {order_field: order_direction}})
    clause_count = len(list(clauses().aggregate(pipeline)))
    if page_size:
        skips = page_size * (page_number - 1)
        pipeline.append({'$skip': skips})
        pipeline.append({'$limit': page_size})
    pipeline.append({
        '$project': {
            '_id': 1,
            'title': 1,
            'level': 1,
            'hiragana': 1,
            'translation': 1
        }
    })
    return clauses().aggregate(pipeline), clause_count


def insert_clause(clause):
    inserted_clause = clauses().insert_one(clause)
    return inserted_clause.inserted_id


def update_clause(clause_id, clause_info):
    clause = clauses().find_one({'_id': ObjectId(clause_id)})
    if clause:
        clauses().update_one({'_id': ObjectId(clause_id)}, {'$set': clause_info})
        return True
    return False


def delete_clause(clause_id):
    return clauses().delete_one({'_id': ObjectId(clause_id)})
