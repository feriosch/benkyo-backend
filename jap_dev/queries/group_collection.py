from jap_dev.information import group_collections


def get_all():
    return group_collections().find()


def check_if_exists(name):
    return group_collections().find({'collection_name': name}).count() > 0


def insert(collection):
    inserted_collection = group_collections().insert_one(collection)
    return inserted_collection.inserted_id
