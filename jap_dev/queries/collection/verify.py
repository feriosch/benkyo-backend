from jap_dev.information import group_collections


def check_if_collection_exists(name):
    return group_collections().find({'collection_name': name}).count() > 0
