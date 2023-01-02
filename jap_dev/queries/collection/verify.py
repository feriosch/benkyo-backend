from jap_dev.information import group_collections


def check_if_collection_exists(name):
    return group_collections().count_documents({'collection_name': name}) > 0
