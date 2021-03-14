from bson.objectid import ObjectId

from jap_dev.information import kanjis, kanji_irregular_components


def get_all():
    return kanjis().find().sort('v1')


def get_from_components(components):
    return kanjis().find({'components': {'$all': components}}).sort('v1')


def get_one_random():
    return kanjis().aggregate([
        {'$sample': {'size': 1}}
    ])


def check_if_kanji_exists(kanji):
    return kanjis().find({'kanji': kanji}).count() > 0


def check_if_spanish_exists(spanish):
    return kanjis().find({'spanish': spanish}).count() > 0


def check_if_v1_exists(v1):
    return kanjis().find({'v1': v1}).count() > 0


def insert(kanji_info):
    inserted_kanji = kanjis().insert_one(kanji_info)
    return inserted_kanji.inserted_id


def find_irregular_radicals(component):
    found_component = kanji_irregular_components().find_one({'component': component})
    if found_component:
        return found_component['radicals']


def fill_radicals(spanish, radicals_list):
    kanji = kanjis().find_one({'spanish': spanish})
    irregular_radicals = find_irregular_radicals(spanish)
    if kanji is None:
        radicals_list.append(spanish)
    else:
        if 'recursive' in kanji:
            radicals_list.append(kanji['spanish'])
        elif irregular_radicals:
            for radical in irregular_radicals:
                radicals_list.append(radical)
        else:
            if 'components' in kanji:
                for component in kanji['components']:
                    fill_radicals(component, radicals_list)
            else:
                radicals_list.append(kanji['spanish'])


def get_radicals(components):
    radicals_list = []
    for component in components:
        fill_radicals(component, radicals_list)
    return radicals_list


def update_kanji(kanji_id, info):
    kanji = kanjis().find_one({'_id': ObjectId(kanji_id)})
    if kanji:
        kanjis().update_one({'_id': ObjectId(kanji_id)}, {'$set': info})
        return True
    return False


def update_kanji_deleting_fields(kanji_id, deleted_fields, info):
    kanji = kanjis().find_one({'_id': ObjectId(kanji_id)})
    if kanji:
        kanjis().update_one(
            {'_id': ObjectId(kanji_id)},
            [
                {'$unset': deleted_fields},
                {'$set': info},
            ],
        )
        return True
    return False


def get_distinct_components():
    return kanjis().distinct('components')
