from jap_dev.information import group_collections


def get_collections():
    return group_collections().find()


def insert_collection(collection):
    inserted_collection = group_collections().insert_one(collection)
    return inserted_collection.inserted_id
