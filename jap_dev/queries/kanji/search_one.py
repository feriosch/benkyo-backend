from bson.objectid import ObjectId

from jap_dev.information import kanjis


def get_one_by_id(kanji_id):
    return kanjis().find_one({'_id': ObjectId(kanji_id)})


def get_one_by_kanji(kanji):
    return kanjis().find_one({'kanji': kanji})


def get_one_random():
    return kanjis().aggregate([
        {'$sample': {'size': 1}}
    ])
