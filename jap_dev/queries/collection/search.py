from jap_dev.information import group_collections


def get_collection_by_name(name):
    return group_collections().find_one({'collection_name': name})
