from jap_dev.information import kanjis


def get_all():
    return kanjis().find()


def get_from_components(components):
    return kanjis().find({'components': {'$all': components}})


def check_if_kanji_exists(kanji):
    return kanjis().find({'kanji': kanji}).count() > 0


def check_if_spanish_exists(spanish):
    return kanjis().find({'spanish': spanish}).count() > 0


def insert(kanji_info):
    inserted_kanji = kanjis().insert_one(kanji_info)
    return inserted_kanji.inserted_id


def search_components(spanish, list):
    kanji = kanjis().find_one({'spanish': spanish})

    if kanji is None:
        list.append(spanish)
    else:
        if 'components' in kanji:
            print(kanji['components'])
            for component in kanji['components']:
                search_components(component, list)
        else:
            list.append(kanji['spanish'])


def get_base_components(spanish):
    components = []
    print(kanjis().find_one({'spanish': spanish})['kanji'])
    search_components(spanish, components)
    return components
