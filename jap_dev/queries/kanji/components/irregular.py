from jap_dev.information import kanji_irregular_components


def get_irregular_components():
    # TODO: Pagination pipelines
    return kanji_irregular_components().find()


def find_irregular_component(component):
    return kanji_irregular_components().find_one({'component': component})
