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
