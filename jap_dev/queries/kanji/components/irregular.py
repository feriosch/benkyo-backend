from jap_dev.information import kanji_irregular_components


def get_irregular_components():
    # TODO: Pagination pipelines
    return kanji_irregular_components().find()


def find_irregular_component(component):
    return kanji_irregular_components().find_one({'component': component})


def check_if_component_exists(component):
    return kanji_irregular_components().count_documents({'component': component}) > 0


def insert_irregular_component(component_info):
    inserted_component = kanji_irregular_components().insert_one(component_info)
    return inserted_component.inserted_id
