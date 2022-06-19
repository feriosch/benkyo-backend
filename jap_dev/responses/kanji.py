from flask import (jsonify)
from bson.objectid import ObjectId

from jap_dev.queries import kanji as queries
from jap_dev.formatters import kanji as formatter
from jap_dev.formatters import id_formatter


def get_kanjis_response(params):
    filter_by = None
    order_field = None
    order_direction = None
    page_size = None
    page_number = None
    components = []
    if 'c1' in params:
        components.append(params['c1'])
    if 'c2' in params:
        components.append(params['c2'])
    if 'c3' in params:
        components.append(params['c3'])
    if 'c4' in params:
        components.append(params['c4'])
    if 'c5' in params:
        components.append(params['c5'])
    if 'c6' in params:
        components.append(params['c6'])
    if 'filter_by' in params:
        filter_by = params['filter_by']
    if 'order_field' in params:
        order_field = params['order_field']
        if 'order_direction' in params:
            if params['order_direction'] == 'ASC':
                order_direction = 1
            elif params['order_direction'] == 'DESC':
                order_direction = -1
            else:
                return {'error': 'Order field must be ASC or DESC'}, 400
        else:
            order_direction = 1
    if 'page_size' in params:
        page_size = int(params['page_size'])
        if page_size < 1 or page_size > 1000:
            return {'error': 'Page size out of boundaries'}, 400
        if 'page_number' in params:
            page_number = int(params['page_number'])
            if page_number < 1:
                return {'error': 'Page number out of boundaries'}, 400
        else:
            page_number = 1

    kanjis, kanji_count = queries.get_kanjis(
        components=components,
        filter_by=filter_by,
        order_field=order_field,
        order_direction=order_direction,
        page_size=page_size,
        page_number=page_number
    )
    formatted_kanjis = formatter.format_all_summarized_kanjis(kanjis)
    page_count, next_page_number = queries.get_pagination_details(
        kanji_count,
        len(formatted_kanjis),
        page_size,
        page_number
    )

    return {
        'kanjis': formatted_kanjis,
        'next_page_number': next_page_number,
        'total_pages': page_count,
        'total_kanjis': kanji_count
    }


def get_one_random_response():
    result = list(queries.get_one_random())
    if not result:
        return {'error': 'No kanjis found'}, 400
    return jsonify(formatter.format_kanji(result[0]))


def get_one_by_id_response(kanji_id):
    if not ObjectId.is_valid(kanji_id):
        return {'error': 'Invalid ID'}, 400
    result = queries.get_one_by_id(kanji_id)
    if result is None:
        return {'error': 'No matched kanji'}, 400
    return jsonify(formatter.format_kanji(result))


def get_one_by_kanji(kanji):
    result = queries.get_one_by_kanji(kanji)
    if result is None:
        return {'error': 'No matched kanji'}, 400
    return jsonify(formatter.format_kanji(result))


def check_if_v1_exists_response(v1):
    return jsonify(queries.check_if_v1_exists(v1))


def check_if_kanji_exists_response(kanji):
    return jsonify(queries.check_if_kanji_exists(kanji))


def check_if_spanish_exists_response(spanish):
    return jsonify(queries.check_if_spanish_exists(spanish))


def create_response(kanji_info):
    if len(kanji_info['kanji']) != 1:
        return {'error': 'Kanji should be just one character'}, 400
    if not kanji_info['spanish'] or str.isspace(kanji_info['spanish']):
        return {'error': 'Invalid spanish'}, 400
    if queries.check_if_v1_exists(kanji_info['v1']):
        return {'error': 'V1 already exists'}, 400
    if queries.check_if_kanji_exists(kanji_info['kanji']):
        return {'error': 'Kanji already exists'}, 400
    if queries.check_if_spanish_exists(kanji_info['spanish']):
        return {'error': 'Spanish already exists'}, 400
    formatted_kanji = formatter.format_kanji_insertion(kanji_info)
    if 'components' in kanji_info:
        formatted_kanji['radicals'] = queries.get_radicals(kanji_info['components'])
    else:
        formatted_kanji['radicals'] = queries.get_radicals([kanji_info['spanish']])
    inserted_id = queries.insert(formatted_kanji)
    return jsonify(id_formatter.format_response_id(inserted_id))


def update_response(kanji_info):
    if len(kanji_info['kanji']) != 1:
        return {'error': 'Kanji should be just one character'}, 400
    if not kanji_info['spanish'] or str.isspace(kanji_info['spanish']):
        return {'error': 'Invalid spanish'}, 400
    kanji_id = kanji_info['kanji_id']
    formatted_kanji = formatter.format_kanji_insertion(kanji_info)
    deleted_fields = formatter.format_deleted_fields(kanji_info)
    if 'components' in kanji_info:
        formatted_kanji['radicals'] = queries.get_radicals(kanji_info['components'])
    else:
        formatted_kanji['radicals'] = queries.get_radicals([kanji_info['spanish']])
    if deleted_fields:
        return jsonify(queries.update_kanji_deleting_fields(kanji_id, deleted_fields, formatted_kanji))
    else:
        return jsonify(queries.update_kanji(kanji_id, formatted_kanji))


def get_distinct_components_response(starting=None, limit=None):
    components = list(queries.get_distinct_components())
    if starting:
        components = list(filter(lambda x: x.startswith(starting), queries.get_distinct_components()))
    if limit:
        components = components[:limit]
    return jsonify(components)
