from jap_dev.queries.kanji.components.irregular import get_irregular_components
from jap_dev.formatters.kanji.components import format_all_irregular_components


def get_irregular_components_response():
    # TODO: Pagination params
    components = get_irregular_components()
    formatted_components = format_all_irregular_components(components)
    return {
        'components': formatted_components
    }
