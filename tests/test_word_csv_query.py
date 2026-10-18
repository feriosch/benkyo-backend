from unittest.mock import MagicMock

import pytest

import jap_dev.queries.word.csv as queries


@pytest.fixture
def collection(monkeypatch):
    collection = MagicMock(name='words')
    monkeypatch.setattr(queries, 'words', lambda: collection)
    return collection


def pipeline_of(collection):
    collection.aggregate.assert_called_once()
    return collection.aggregate.call_args.args[0]


def stage(pipeline, name):
    return [s[name] for s in pipeline if name in s]


def test_no_filters_has_only_lookup_and_project(collection):
    queries.get_words_for_csv(None, [], True)
    pipeline = pipeline_of(collection)
    assert stage(pipeline, '$match') == []
    assert pipeline[0] == queries.related_lookup
    assert '$project' in pipeline[-1]


def test_group_and_tags_filters(collection):
    queries.get_words_for_csv('jlpt_n2', ['common', 'expression'], True)
    matches = stage(pipeline_of(collection), '$match')
    assert {'group': 'jlpt_n2'} in matches
    assert {'tags': {'$all': ['common', 'expression']}} in matches


@pytest.mark.parametrize('fetch', [
    lambda: queries.get_words_for_csv(None, [], True),
    lambda: queries.get_jlpt_words_for_csv(True),
])
def test_projection_exports_object_id_as_string(collection, fetch):
    fetch()
    project = stage(pipeline_of(collection), '$project')[0]
    assert project['_id'] == 0
    assert project['id'] == {'$toString': '$_id'}


@pytest.mark.parametrize('fetch', [
    lambda kana: queries.get_words_for_csv(None, [], kana),
    lambda kana: queries.get_jlpt_words_for_csv(kana),
])
def test_usually_kana_switches_word_and_reading(collection, fetch):
    fetch(True)
    project = stage(pipeline_of(collection), '$project')[0]
    assert project['word'] == queries.projections['word']
    assert project['hiragana'] == queries.projections['hiragana']

    collection.reset_mock()
    fetch(False)
    project = stage(pipeline_of(collection), '$project')[0]
    assert project['word'] == 1
    assert project['hiragana'] == 1


@pytest.mark.parametrize('fetch', [
    lambda: queries.get_words_for_csv(None, [], True),
    lambda: queries.get_jlpt_words_for_csv(True),
])
def test_projection_keeps_fields_the_formatter_needs(collection, fetch):
    fetch()
    project = stage(pipeline_of(collection), '$project')[0]
    for field in ('spanish', 'type', 'tags', 'notes', 'related', '_relatedWords'):
        assert project[field] == 1
    assert project['sentence'] == {'$first': '$sentences.sentence'}
    assert project['translation'] == {'$first': '$sentences.translation'}


@pytest.mark.parametrize('fetch', [
    lambda: queries.get_words_for_csv(None, [], True),
    lambda: queries.get_jlpt_words_for_csv(True),
])
def test_projection_passes_unswapped_answer_forms(collection, fetch):
    fetch()
    project = stage(pipeline_of(collection), '$project')[0]
    assert project['answer_word'] == '$word'
    assert project['answer_reading'] == '$hiragana'


def test_jlpt_match_covers_jlpt_groups_and_n1_tag(collection):
    queries.get_jlpt_words_for_csv(True)
    match = stage(pipeline_of(collection), '$match')[0]
    assert match == {'$or': [
        {'group': 'jlpt_n3'},
        {'group': 'jlpt_n2'},
        {'group': 'jlpt_n1'},
        {'tags': {'$all': ['jlpt_n1']}},
    ]}


def test_related_lookup_joins_words_by_object_id():
    lookup = queries.related_lookup['$lookup']
    assert lookup['from'] == 'words'
    assert lookup['localField'] == 'related.wordId'
    assert lookup['foreignField'] == '_id'
    assert lookup['as'] == '_relatedWords'
