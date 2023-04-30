def format_irregular_component(component):
    return {
        'id': str(component['_id']),
        'component': component['component'],
        'radicals': component['radicals']
    }


def format_all_irregular_components(components):
    result = []
    for component in components:
        result.append(format_irregular_component(component))
    return result


def format_irregular_component_insertion(component_info):
    formatted_object = dict()
    formatted_object['component'] = component_info['component']
    formatted_object['radicals'] = component_info['radicals']
    return formatted_object
