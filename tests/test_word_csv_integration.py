"""Runs the real CSV pipelines against MongoDB. Read-only (aggregate only).

Skipped unless BENKYO_TEST_MONGODB_URI is set, e.g.:
    BENKYO_TEST_MONGODB_URI="$MONGODB_URI" .venv/Scripts/python -m pytest tests/test_word_csv_integration.py
"""
import os
import re

import pytest
from pandas import DataFrame

import jap_dev.queries.word.csv as queries
from jap_dev.formatters.word.csv import format_all_csv_words
from jap_dev.responses.word.csv import csv_columns

URI = os.getenv('BENKYO_TEST_MONGODB_URI')

pytestmark = pytest.mark.skipif(not URI, reason='BENKYO_TEST_MONGODB_URI not set')


@pytest.fixture(scope='module')
def real_words():
    from pymongo import MongoClient
    client = MongoClient(URI, serverSelectionTimeoutMS=10000)
    yield client.get_database()['words']
    client.close()


@pytest.fixture
def use_real_db(monkeypatch, real_words):
    monkeypatch.setattr(queries, 'words', lambda: real_words)
    return real_words


@pytest.mark.parametrize('usually_kana', [True, False])
def test_jlpt_export_on_real_data(use_real_db, usually_kana):
    docs = list(queries.get_jlpt_words_for_csv(usually_kana))
    assert docs, 'expected JLPT words in the database'

    ids = [doc['id'] for doc in docs]
    assert all(re.fullmatch(r'[0-9a-f]{24}', i) for i in ids)
    assert len(set(ids)) == len(ids)
    assert all('_id' not in doc for doc in docs)

    df = DataFrame.from_dict(format_all_csv_words(docs)).reindex(columns=csv_columns)
    assert len(df) == len(docs)
    assert df['id'].notna().all()
    assert df['word'].notna().all()


def test_related_lookup_resolves_db_edges(use_real_db):
    doc = use_real_db.find_one({'related.wordId': {'$exists': True}}, {'_id': 1, 'group': 1})
    if not doc:
        pytest.skip('no word with DB-linked related words')
    exported = [d for d in queries.get_words_for_csv(doc['group'], [], True) if d['id'] == str(doc['_id'])]
    assert len(exported) == 1
    assert exported[0]['_relatedWords'], 'lookup should resolve related.wordId'
