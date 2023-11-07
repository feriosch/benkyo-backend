from jap_dev.information import words


def check_if_word_exists(word):
    return words().count_documents({'word': word}) > 0


# TODO: Check this out
def check_if_collection_exists(collection):
    return collection in words().distinct('group')
