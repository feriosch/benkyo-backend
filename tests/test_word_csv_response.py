import csv
import re
from pathlib import Path

import pytest
from bson import ObjectId

import jap_dev.responses.word.csv as responses

ANKI_DIR = Path(__file__).resolve().parent.parent / 'anki'


def db_word(**overrides):
    """A word as returned by the CSV aggregation (after $project)."""
    word = {
        'id': str(ObjectId()),
        'word': '一層',
        'hiragana': 'いっそう',
        'spanish': 'aún más, mucho más (formal)',
        'type': {'adv': 1},
        'tags': ['common'],
        'sentence': '前より一層努力しなければならない。',
        'translation': 'Tengo que esforzarme aún más que antes.',
        'notes': 'Más formal que もっと.',
        'related': [],
        '_relatedWords': [],
    }
    word.update(overrides)
    return word


@pytest.fixture
def fake_words(monkeypatch):
    """Replace both queries; records the arguments and returns the given words."""
    state = {'words': [db_word()], 'calls': []}

    def get_words(collection, tags, usually_kana):
        state['calls'].append(('main', collection, tags, usually_kana))
        return iter(state['words'])

    def get_jlpt_words(usually_kana):
        state['calls'].append(('jlpt', usually_kana))
        return iter(state['words'])

    monkeypatch.setattr(responses, 'get_words_for_csv', get_words)
    monkeypatch.setattr(responses, 'get_jlpt_words_for_csv', get_jlpt_words)
    return state


def read_csv(path):
    lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
    header = [line.rstrip('\r\n') for line in lines if line.startswith('#')]
    rows = list(csv.reader(line for line in lines if not line.startswith('#')))
    return header, rows


# Anki header and columns

def test_anki_fields_match_csv_columns():
    assert len(responses.anki_fields) == len(responses.csv_columns)
    assert responses.csv_columns[0] == 'id'
    assert responses.anki_fields[0] == 'Id'


def test_file_starts_with_anki_header(fake_words, files_dir):
    responses.get_words_csv_response({})
    header, _ = read_csv(files_dir / 'benkyo.csv')
    assert header == [
        '#separator:Comma',
        '#html:true',
        '#columns:' + ','.join(responses.anki_fields),
    ]


def test_header_lines_come_first(fake_words, files_dir):
    responses.get_words_csv_response({})
    lines = (files_dir / 'benkyo.csv').read_text(encoding='utf-8').splitlines()
    assert [line.startswith('#') for line in lines] == [True, True, True, False]


def test_row_values_in_column_order(fake_words, files_dir):
    word = db_word(tags=['common', 'jlpt_n1', 'transitive', 'rare'])
    fake_words['words'] = [word]
    responses.get_words_csv_response({})
    _, rows = read_csv(files_dir / 'benkyo.csv')

    assert len(rows) == 1
    row = dict(zip(responses.anki_fields, rows[0]))
    assert row == {
        'Id': word['id'],
        'Word': '一層',
        'Pronunciation': 'いっそう',
        'Definition': 'aún más, mucho más (formal)',
        'Type': '副',
        'Notes': 'Más formal que もっと.',
        'Japanese Sentence': '前より一層努力しなければならない。',
        'Translation Sentence': 'Tengo que esforzarme aún más que antes.',
        'Common': 'True',
        'JLPT N1': 'True',
        'Expression': '',
        'Onomatopoeic': '',
        'Transitive': 'True',
        'Intransitive': '',
        'Related Front': '',
        'Related Back': '',
        'Usage': '<span class="tag usage">Rare</span>',
    }


def test_every_row_has_one_value_per_field(fake_words, files_dir):
    fake_words['words'] = [db_word(), db_word(tags=[], sentence=None, translation=None, notes='')]
    responses.get_words_csv_response({})
    _, rows = read_csv(files_dir / 'benkyo.csv')
    assert [len(row) for row in rows] == [len(responses.anki_fields)] * 2


def test_ids_are_unique_per_row(fake_words, files_dir):
    fake_words['words'] = [db_word(), db_word(), db_word()]
    responses.get_words_csv_response({})
    _, rows = read_csv(files_dir / 'benkyo.csv')
    ids = [row[0] for row in rows]
    assert len(set(ids)) == 3
    assert all(re.fullmatch(r'[0-9a-f]{24}', i) for i in ids)


def test_commas_quotes_and_newlines_survive(fake_words, files_dir):
    fake_words['words'] = [db_word(spanish='a, "b"', notes='línea 1\nlínea 2')]
    responses.get_words_csv_response({})
    _, rows = read_csv(files_dir / 'benkyo.csv')
    row = dict(zip(responses.anki_fields, rows[0]))
    assert row['Definition'] == 'a, "b"'
    assert row['Notes'] == 'línea 1\nlínea 2'


def test_related_html_is_exported(fake_words, files_dir):
    rel_id = ObjectId()
    fake_words['words'] = [db_word(
        related=[{'wordId': rel_id, 'type': 'related', 'note': 'en mayor grado'}],
        _relatedWords=[{'_id': rel_id, 'word': '一段と', 'group': 'jlpt_n2'}],
    )]
    responses.get_words_csv_response({})
    _, rows = read_csv(files_dir / 'benkyo.csv')
    row = dict(zip(responses.anki_fields, rows[0]))
    assert '■段と' in row['Related Front'] and 'en mayor grado' not in row['Related Front']
    assert '一段と' in row['Related Back'] and 'en mayor grado' in row['Related Back']


# get_words_csv_response parameters

def test_default_params(fake_words, files_dir):
    assert responses.get_words_csv_response({}) == 'benkyo'
    assert fake_words['calls'] == [('main', None, [], True)]
    assert (files_dir / 'benkyo.csv').exists()


def test_group_names_the_file_and_filters(fake_words, files_dir):
    assert responses.get_words_csv_response({'group': 'jlpt_n2'}) == 'jlpt_n2'
    assert fake_words['calls'] == [('main', 'jlpt_n2', [], True)]
    assert (files_dir / 'jlpt_n2.csv').exists()


def test_tags_are_collected_in_order(fake_words, files_dir):
    responses.get_words_csv_response({'tag_1': 'common', 'tag_3': 'expression', 'tag_2': 'rare'})
    assert fake_words['calls'][0][2] == ['common', 'rare', 'expression']


@pytest.mark.parametrize('value, expected', [('true', True), ('True', True), ('false', False), ('False', False)])
def test_usually_kana_param(fake_words, files_dir, value, expected):
    responses.get_words_csv_response({'usually_kana': value})
    assert fake_words['calls'][0][3] is expected


def test_no_words_returns_false_and_writes_nothing(fake_words, files_dir):
    fake_words['words'] = []
    assert responses.get_words_csv_response({}) is False
    assert not (files_dir / 'benkyo.csv').exists()


# get_jlpt_words_csv_response

def test_jlpt_writes_jlpt_csv(fake_words, files_dir):
    assert responses.get_jlpt_words_csv_response({}) is True
    assert fake_words['calls'] == [('jlpt', True)]
    header, rows = read_csv(files_dir / 'jlpt.csv')
    assert header[2] == '#columns:' + ','.join(responses.anki_fields)
    assert len(rows) == 1


def test_jlpt_usually_kana_false(fake_words, files_dir):
    responses.get_jlpt_words_csv_response({'usually_kana': 'false'})
    assert fake_words['calls'] == [('jlpt', False)]


def test_jlpt_no_words_returns_false(fake_words, files_dir):
    fake_words['words'] = []
    assert responses.get_jlpt_words_csv_response({}) is False


# Contract with the Anki templates in anki/

def template_fields(path):
    return {name.strip() for name in re.findall(r'\{\{[#/^]?([^}]+)\}\}', path.read_text(encoding='utf-8'))}


def test_templates_only_use_exported_fields():
    special = {'FrontSide'}
    for template in ANKI_DIR.glob('*/*.html'):
        unknown = template_fields(template) - set(responses.anki_fields) - special
        assert not unknown, f'{template.relative_to(ANKI_DIR)} uses fields not in the CSV: {unknown}'


def test_templates_never_show_the_id():
    for template in ANKI_DIR.glob('*/*.html'):
        assert 'Id' not in template_fields(template), template.name


def test_related_fields_are_on_the_expected_sides():
    assert 'Related Front' in template_fields(ANKI_DIR / 'definition_card' / 'front.html')
    assert 'Related Back' in template_fields(ANKI_DIR / 'definition_card' / 'back.html')
    assert 'Related Back' in template_fields(ANKI_DIR / 'word_card' / 'back.html')
    assert 'Related Back' not in template_fields(ANKI_DIR / 'definition_card' / 'front.html')
    assert 'Related Back' not in template_fields(ANKI_DIR / 'word_card' / 'front.html')


def test_readme_lists_fields_in_csv_order():
    readme = (ANKI_DIR / 'README.md').read_text(encoding='utf-8')
    listed = re.findall(r'^\d+\. (.+)$', readme, flags=re.M)
    assert listed == responses.anki_fields
