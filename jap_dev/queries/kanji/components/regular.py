from jap_dev.information import kanjis


def get_from_components(components):
    return kanjis().find({'components': {'$all': components}}).sort('v1')


def get_distinct_components():
    return kanjis().distinct('components')
