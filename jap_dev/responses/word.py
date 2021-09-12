from flask import (jsonify)
from bson.objectid import ObjectId
from pandas import DataFrame

from jap_dev.queries import word as queries
from jap_dev.formatters import word as formatter
from jap_dev.formatters import id_formatter


def get_words_response(params):
    collection = None
    filter_by = None
    order_field = None
    order_direction = None
    page_size = None
    page_number = None

    if 'from' in params and params['from'] != 'all':
        collection = params['from']
        if not queries.check_if_collection_exists(collection):
            return {'error': 'Collection not found'}, 400
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

    words, word_count = queries.get_words(
        collection=collection,
        filter_by=filter_by,
        order_field=order_field,
        order_direction=order_direction,
        page_size=page_size,
        page_number=page_number
    )
    formatted_words = formatter.format_all_words(words)
    page_count, next_page_number = queries.get_pagination_details(
        word_count,
        len(formatted_words),
        page_size,
        page_number
    )

    return {
        'words': formatted_words,
        'next_page_number': next_page_number,
        'total_pages': page_count,
        'total_words': word_count
    }


def create_word_response(word_info):
    if queries.check_if_word_exists(word_info['word']):
        return {'error': 'Word repeated'}, 400
    if word_info['from'] == 'all':
        return {'error': 'Bad collection input: all is not allowed'}, 400
    formatted_word = formatter.format_word_insertion(word_info)
    inserted_id = queries.insert(formatted_word)
    return jsonify(id_formatter.format_response_id(inserted_id))


def search_one_by_word_response(word):
    result = queries.search_one_by_word(word)
    if result is None:
        return jsonify(result)
    return jsonify(formatter.format_word(result))


def search_one_by_id_response(word_id):
    if not ObjectId.is_valid(word_id):
        return {'error': 'Invalid ID'}, 400
    result = queries.search_one_by_id(word_id)
    if result is None:
        return {'error': 'No matched word'}, 400
    return jsonify(formatter.format_word(result))


def search_one_random_by_collection_response(collection):
    result = list(queries.search_one_random_by_collection(collection))
    if not result:
        return {'error': 'No words found in collection'}, 400
    return jsonify(formatter.format_word(result[0]))


def search_one_random_response():
    result = list(queries.search_one_random())
    if not result:
        return {'error': 'No words found'}, 400
    return jsonify(formatter.format_word(result[0]))


def search_many_response(word):
    result = queries.search_many(word)
    return jsonify(formatter.format_all_words(result))


def update_word_response(word_info):
    word_id = word_info['word_id']
    formatted_word = formatter.format_word_update(word_info)
    if queries.update_word(word_id, formatted_word):
        return {'id': word_id}, 200
    return {'error': 'No matched word'}, 400


def update_level_response(word_id, success):
    bool_success = bool(int(success))
    if queries.update_word_level(word_id, bool_success):
        return {'id': word_id}, 200
    return {'error': 'No matched word'}, 400


def csv_response(collection):
    df = DataFrame.from_dict(queries.get_words_for_csv(collection))
    if not df.empty:
        if collection:
            df.to_csv(f'./{collection}.csv', index=False, header=False)
        else:
            df.to_csv('./benkyo.csv', index=False, header=False)
        return {'message': f'Success. Saved as {collection}.csv'}, 200
    return {'error': 'CSV error'}, 400
