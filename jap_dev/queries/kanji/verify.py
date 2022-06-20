from jap_dev.information import kanjis


def check_if_kanji_exists(kanji):
    return kanjis().find({'kanji': kanji}).count() > 0


def check_if_spanish_exists(spanish):
    return kanjis().find({'spanish': spanish}).count() > 0


def check_if_v1_exists(v1):
    return kanjis().find({'v1': v1}).count() > 0
