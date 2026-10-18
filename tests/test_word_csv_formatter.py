from bson import ObjectId

from jap_dev.formatters.word.csv import (
    MASK_CHAR, clean_notes, format_csv_word, format_related, format_type, format_usage, mask_answer,
    _mask_shared_kanji
)


def related_word(word, group='basic', tags=None, hiragana=None):
    return {'_id': ObjectId(), 'word': word, 'hiragana': hiragana, 'group': group, 'tags': tags or []}


# format_type

def test_format_type_maps_subtypes_in_order():
    assert format_type({'noun': 1, 'suru': 1}) == '名、する'


def test_format_type_to_and_teki_variants():
    assert format_type({'adv': 4}) == '副と'
    assert format_type({'na_adj': 5}) == 'な形的'


def test_format_type_ignores_unknown_keys_and_zero_values():
    assert format_type({'noun': 0, 'unknown': 1, 'verb': 1}) == '動'


# _mask_shared_kanji

def test_mask_replaces_only_kanji_shared_with_target():
    assert _mask_shared_kanji('一段と', '一層') == f'{MASK_CHAR}段と'


def test_mask_keeps_kana_even_if_target_has_it():
    assert _mask_shared_kanji('もっと', 'もっと') == 'もっと'


def test_mask_without_kanji_in_target_returns_word():
    assert _mask_shared_kanji('一層', 'いっそう') == '一層'


# mask_answer

def test_mask_answer_hides_word_and_shared_kanji():
    assert mask_answer('(S が) ～を 敬う', '敬う', 'うやまう') == '(S が) ～を ■■'
    assert mask_answer('巧み: habil', '巧妙', 'こうみょう') == '■み: habil'


def test_mask_answer_hides_reading_in_hiragana_and_katakana():
    assert mask_answer('S が (何に) こだわる', '拘る', 'こだわる') == 'S が (何に) ■■■■'
    assert mask_answer('tambien ガンガン', 'ガンガン', 'がんがん') == 'tambien ■■■■'
    assert mask_answer('abr. de ボトルネック', 'ネック', None) == 'abr. de ボトル■■■'


def test_mask_answer_hides_stem_of_inflecting_words():
    assert mask_answer('こだわり, こだわって', '拘る', 'こだわる') == '■■■り, ■■■って'
    assert mask_answer('はかなさ', '儚い', 'はかない') == '■■■さ'


def test_mask_answer_keeps_kana_of_words_without_okurigana():
    # 期待 ends in a kanji, so the い of きたい is not an inflection
    assert mask_answer('きた, きたい', '期待', 'きたい') == 'きた, ■■■'


def test_mask_answer_skips_one_kana_readings():
    assert mask_answer('きのこ, き', '木', 'き') == 'きのこ, き'


def test_mask_answer_masks_longest_form_first():
    assert mask_answer('かく、掻く', '掻く', 'かく') == '■■、■■'


def test_mask_answer_leaves_unrelated_text_and_empty_values():
    assert mask_answer('Más formal que もっと.', '一層', 'いっそう') == 'Más formal que もっと.'
    assert mask_answer('', '一層', 'いっそう') == ''
    assert mask_answer(None, '一層', 'いっそう') is None


# format_related

def test_format_related_without_related_returns_empty_strings():
    assert format_related({'word': '一層'}) == ('', '')
    assert format_related({'word': '一層', 'related': []}) == ('', '')


def test_format_related_db_edge_masks_front_and_shows_note_on_back():
    rel = related_word('一段と', group='jlpt_n2')
    word = {
        'word': '一層',
        'related': [{'wordId': rel['_id'], 'type': 'related', 'note': 'en mayor grado'}],
        '_relatedWords': [rel],
    }
    front, back = format_related(word)

    assert front.startswith('<ul class="related-list">') and front.endswith('</ul>')
    assert f'<span class="rel-word">{MASK_CHAR}段と</span>' in front
    assert 'en mayor grado' not in front
    assert '<span class="rel-word">一段と</span>' in back
    assert '<span class="rel-note">en mayor grado</span>' in back
    assert '<span class="rel-level">N2</span>' in front and '<span class="rel-level">N2</span>' in back


def test_format_related_type_prefix_and_class():
    syn, ant = related_word('もっと'), related_word('少し')
    word = {
        'word': '一層',
        'related': [
            {'wordId': syn['_id'], 'type': 'synonym', 'note': ''},
            {'wordId': ant['_id'], 'type': 'antonym', 'note': ''},
            {'word': '層', 'type': 'related', 'note': ''},
        ],
        '_relatedWords': [syn, ant],
    }
    _, back = format_related(word)

    assert '<li class="rel rel-synonym"><span class="rel-head"><span class="rel-type">=</span>' in back
    assert '<li class="rel rel-antonym"><span class="rel-head"><span class="rel-type">✕</span>' in back
    assert '<li class="rel rel-related"><span class="rel-head"><span class="rel-type">~</span>' in back


def test_format_related_keeps_db_order():
    a, b = related_word('もっと'), related_word('更に')
    word = {
        'word': '一層',
        'related': [{'wordId': b['_id'], 'type': 'related'}, {'wordId': a['_id'], 'type': 'related'}],
        '_relatedWords': [a, b],
    }
    _, back = format_related(word)
    assert back.index('更に') < back.index('もっと')


def test_format_related_nuance_tags_on_both_sides():
    rel = related_word('もっと')
    word = {
        'word': '一層',
        'related': [{'wordId': rel['_id'], 'type': 'synonym', 'note': 'x', 'tags': ['casual', 'spoken']}],
        '_relatedWords': [rel],
    }
    expected = '<span class="rel-tags"><span class="rel-tag">casual</span><span class="rel-tag">spoken</span></span>'
    front, back = format_related(word)
    assert expected in front and expected in back


def test_format_related_jlpt_labels():
    n1_group = related_word('甚だ', group='jlpt_n1')
    n1_tag = related_word('囁く', group='literature', tags=['jlpt_n1'])
    n3 = related_word('更に', group='jlpt_n3')
    basic = related_word('もっと', group='basic')
    word = {
        'word': '一層',
        'related': [{'wordId': w['_id'], 'type': 'related'} for w in (n1_group, n1_tag, n3, basic)],
        '_relatedWords': [n1_group, n1_tag, n3, basic],
    }
    _, back = format_related(word)
    items = back.split('</li>')

    assert '<span class="rel-level">N1</span>' in items[0]
    assert '<span class="rel-level">N1</span>' in items[1]
    assert '<span class="rel-level">N3</span>' in items[2]
    assert 'rel-level' not in items[3]


def test_format_related_falls_back_to_hiragana_when_word_missing():
    rel = related_word(None, hiragana='もっと')
    word = {'word': '一層', 'related': [{'wordId': rel['_id'], 'type': 'related'}], '_relatedWords': [rel]}
    _, back = format_related(word)
    assert '<span class="rel-word">もっと</span>' in back


def test_format_related_basic_edge_has_no_level_and_is_masked():
    word = {'word': '天気', 'related': [{'word': '天候', 'type': 'synonym', 'note': 'formal'}], '_relatedWords': []}
    front, back = format_related(word)
    assert f'<span class="rel-word">{MASK_CHAR}候</span>' in front
    assert '<span class="rel-word">天候</span>' in back
    assert 'rel-level' not in back


def test_format_related_masks_usually_kana_card_with_db_forms():
    # usually_kana export: word is already kana, the DB forms come in answer_*
    rel = related_word('拘り')
    word = {'word': 'こだわる', 'answer_word': '拘る', 'answer_reading': 'こだわる',
            'related': [{'wordId': rel['_id'], 'type': 'related'}, {'word': 'こだわり', 'type': 'related'}],
            '_relatedWords': [rel]}
    front, back = format_related(word)
    assert f'<span class="rel-word">{MASK_CHAR}り</span>' in front
    assert '<span class="rel-word">こだわり</span>' not in front
    assert '<span class="rel-word">拘り</span>' in back and '<span class="rel-word">こだわり</span>' in back


def test_format_related_skips_dangling_ids():
    word = {'word': '一層', 'related': [{'wordId': ObjectId(), 'type': 'related'}], '_relatedWords': []}
    assert format_related(word) == ('<ul class="related-list"></ul>', '<ul class="related-list"></ul>')


# format_usage

def test_format_usage_skips_column_tags_and_labels_the_rest():
    tags = ['common', 'jlpt_n1', 'usually_kana', 'transitive', 'joyogai', 'elderly_speech']
    assert format_usage(tags) == (
        '<span class="tag usage">Not Joyo</span>'
        '<span class="tag usage">Elderly speech</span>'
    )


def test_format_usage_empty():
    assert format_usage([]) == ''
    assert format_usage(['common']) == ''


# clean_notes

def test_clean_notes_removes_legacy_relation_text():
    assert clean_notes('rel: なおさら; Más formal que もっと') == 'Más formal que もっと'
    assert clean_notes('Uso escrito; sinonimo: 更に') == 'Uso escrito'
    assert clean_notes('ANTONIMO: 少し') == ''


def test_clean_notes_keeps_plain_notes_and_empty_values():
    assert clean_notes('Más formal que もっと.') == 'Más formal que もっと.'
    assert clean_notes('') == ''
    assert clean_notes(None) is None


# format_csv_word

def test_format_csv_word_sets_flag_columns_and_drops_internal_fields():
    rel = related_word('もっと')
    word = {
        'id': '64b000000000000000000001',
        'word': '一層',
        'hiragana': 'いっそう',
        'type': {'adv': 1},
        'tags': ['common', 'jlpt_n1', 'expression', 'onomatopoeic', 'transitive', 'intransitive', 'rare'],
        'notes': 'rel: もっと',
        'related': [{'wordId': rel['_id'], 'type': 'synonym'}],
        '_relatedWords': [rel],
    }
    result = format_csv_word(word)

    assert result['id'] == '64b000000000000000000001'
    assert result['type'] == '副'
    for flag in ('common', 'jlpt_n1', 'expression', 'onomatopoeic', 'transitive', 'intransitive'):
        assert result[flag] is True
    assert result['usage'] == '<span class="tag usage">Rare</span>'
    assert result['notes'] == ''
    assert result['notes_front'] == ''
    assert 'もっと' in result['related_front'] and 'もっと' in result['related_back']
    assert 'related' not in result and '_relatedWords' not in result


def test_format_csv_word_masks_notes_front_only():
    result = format_csv_word({'id': 'x', 'word': '敬う', 'hiragana': 'うやまう', 'answer_word': '敬う',
                              'answer_reading': 'うやまう', 'notes': '(S が) ～を 敬う'})
    assert result['notes'] == '(S が) ～を 敬う'
    assert result['notes_front'] == '(S が) ～を ■■'
    assert 'answer_word' not in result and 'answer_reading' not in result


def test_format_csv_word_without_tags_or_type():
    result = format_csv_word({'id': 'x', 'word': '一層', 'notes': 'n'})
    assert 'common' not in result
    assert 'usage' not in result
    assert result['related_front'] == '' and result['related_back'] == ''
    assert result['notes'] == 'n'
