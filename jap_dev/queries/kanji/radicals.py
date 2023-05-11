from jap_dev.information import kanjis
from jap_dev.queries.kanji.components.irregular import find_irregular_component


def find_irregular_radicals(component):
    found_component = find_irregular_component(component)
    if found_component:
        return found_component['radicals']


def fill_radicals(spanish, radicals_list):
    kanji = kanjis().find_one({'spanish': spanish})
    irregular_radicals = find_irregular_radicals(spanish)
    if kanji is None:
        if irregular_radicals:
            for radical in irregular_radicals:
                radicals_list.append(radical)
        else:
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


def get_distinct_radicals():
    return kanjis().distinct('radicals')
