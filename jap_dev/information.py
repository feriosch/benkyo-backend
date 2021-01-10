from jap_dev.helpers.connection import database


def group_collections():
    return database['group_collections']


def words():
    return database['words']


def users():
    return database['users']


def kanjis():
    return database['kanjis']


def kanji_irregular_components():
    return database['kanjiIrregularComponents']
