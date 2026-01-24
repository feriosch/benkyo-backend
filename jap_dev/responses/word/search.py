from flask import (jsonify)
from bson.objectid import ObjectId

import jap_dev.queries.word.search as queries
from jap_dev.formatters.word.main import format_word
from jap_dev.information import words


def fetch_related_words(word_doc):
    if 'related' not in word_doc or not word_doc['related']:
        return {}
    
    # Extract all related word IDs
    related_ids = [rel['wordId'] for rel in word_doc['related'] if 'wordId' in rel]
    
    if not related_ids:
        return {}
    
    # Fetch all related words in one query
    related_docs = words().find(
        {'_id': {'$in': related_ids}},
        {'word': 1, 'hiragana': 1, 'spanish': 1}
    )
    
    # Build lookup dict
    return {str(doc['_id']): doc for doc in related_docs}


def get_one_random_response():
    result = list(queries.get_one_random())
    if not result:
        return {'error': 'No words found'}, 400
    word_doc = result[0]
    related_words = fetch_related_words(word_doc)
    return jsonify(format_word(word_doc, related_words))


def get_one_by_id_response(word_id):
    if not ObjectId.is_valid(word_id):
        return {'error': 'Invalid ID'}, 400
    result = queries.get_one_by_id(word_id)
    if result is None:
        return {'error': 'No matched word'}, 400
    related_words = fetch_related_words(result)
    return jsonify(format_word(result, related_words))


def get_one_by_word_response(word):
    result = queries.get_one_by_word(word)
    if result is None:
        return jsonify(result)
    related_words = fetch_related_words(result)
    return jsonify(format_word(result, related_words))


def get_one_random_by_collection_response(collection):
    result = list(queries.get_one_random_by_collection(collection))
    if not result:
        return {'error': 'No words found in collection'}, 400
    word_doc = result[0]
    related_words = fetch_related_words(word_doc)
    return jsonify(format_word(word_doc, related_words))
