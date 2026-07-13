import re
import unicodedata


TYPE_PREFIXES = {'synonym': '=', 'antonym': '✕', 'related': '~'}

JLPT_LABELS = {
    'jlpt_n1': 'N1',
    'jlpt_n2': 'N2',
    'jlpt_n3': 'N3',
}

REL_NOTE_PATTERNS = [
    r'rel:\s*[^;]+(?:;|$)',
    r'sinonimo:\s*[^;]+(?:;|$)',
    r'antonimo:\s*[^;]+(?:;|$)',
]

MASK_CHAR = '■'


def _is_kanji(ch):
    cp = ord(ch)
    return (0x4E00 <= cp <= 0x9FFF or
            0x3400 <= cp <= 0x4DBF or
            0x20000 <= cp <= 0x2A6DF)


def _mask_shared_kanji(rel_word, target_word):
    target_kanji = {ch for ch in target_word if _is_kanji(ch)}
    if not target_kanji:
        return rel_word
    return ''.join(MASK_CHAR if (ch in target_kanji and _is_kanji(ch)) else ch for ch in rel_word)


def _build_item(prefix, rel_word, nuance_tags, jlpt_label, note=None, rel_type='related'):
    level_html = f'<span class="rel-level">{jlpt_label}</span>' if jlpt_label else ''
    tags_html = ''
    if nuance_tags:
        tags_html = ''.join(f'<span class="rel-tag">{tag}</span>' for tag in nuance_tags)
        tags_html = f'<span class="rel-tags">{tags_html}</span>'
    head = (
        '<span class="rel-head">'
        f'<span class="rel-type">{prefix}</span>'
        f'<span class="rel-word">{rel_word}</span>'
        f'{level_html}{tags_html}'
        '</span>'
    )
    note_html = f'<span class="rel-note">{note}</span>' if note else ''
    return f'<li class="rel rel-{rel_type}">{head}{note_html}</li>'


def format_related(word):
    """Returns (masked_html, full_html) for front/back of Anki cards."""
    related = word.get('related', [])
    lookup = word.get('_relatedWords', [])
    if not related:
        return '', ''

    target_word = word.get('word', '')

    word_map = {}
    for w in lookup:
        oid = str(w['_id'])
        word_map[oid] = {
            'word': w.get('word') or w.get('hiragana', '?'),
            'group': w.get('group', ''),
        }

    front_items = []
    back_items = []
    for rel in related:
        word_id = str(rel.get('wordId', ''))
        entry = word_map.get(word_id)

        if entry:
            rel_word = entry['word']
            jlpt_label = JLPT_LABELS.get(entry['group'], '')
        elif rel.get('word'):
            rel_word = rel['word']
            jlpt_label = ''
        else:
            continue

        rel_type = rel.get('type', 'related')
        nuance_tags = rel.get('tags', [])
        note = rel.get('note', '')
        prefix = TYPE_PREFIXES.get(rel_type, '~')

        # The back of the card also shows the free-text nuance note (usage
        # preferences, register, position) for reference; the front stays clean.
        back_items.append(_build_item(prefix, rel_word, nuance_tags, jlpt_label, note, rel_type))

        masked_word = _mask_shared_kanji(rel_word, target_word)
        front_items.append(_build_item(prefix, masked_word, nuance_tags, jlpt_label, None, rel_type))

    wrap = lambda items: '<ul class="related-list">' + ''.join(items) + '</ul>'
    return wrap(front_items), wrap(back_items)


def clean_notes(notes):
    if not notes:
        return notes
    cleaned = notes
    for pattern in REL_NOTE_PATTERNS:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'^[;,\s]+|[;,\s]+$', '', cleaned)
    cleaned = re.sub(r'\s*;\s*$', '', cleaned)
    return cleaned.strip()


def format_type(word_type):
    formatted_type = []
    japanese_subtypes = {
        'noun': '名',
        'suru': 'する',
        'no_adj': 'の形',
        'na_adj': 'な形',
        'i_adj': 'い形',
        'adv': '副',
        'verb': '動',
        'adj_noun': '名形',
        'adv_noun': '副名',
        'counter': '回'
    }
    to_subtype = 'と'
    teki_subtype = '的'
    for key, value in word_type.items():
        if value == 1 and key in japanese_subtypes:
            formatted_type.append(japanese_subtypes[key])
        if value == 4 and key in japanese_subtypes:
            formatted_type.append(japanese_subtypes[key] + to_subtype)
        if value == 5 and key in japanese_subtypes:
            formatted_type.append(japanese_subtypes[key] + teki_subtype)
    return '、'.join(formatted_type)


def format_csv_word(word):
    formatted_word = word
    if 'type' in word:
        formatted_word['type'] = format_type(word['type'])
    if 'tags' in word:
        if 'common' in word['tags']:
            formatted_word['common'] = True
        if 'jlpt_n1' in word['tags']:
            formatted_word['jlpt_n1'] = True
        if 'expression' in word['tags']:
            formatted_word['expression'] = True
        if 'onomatopoeic' in word['tags']:
            formatted_word['onomatopoeic'] = True
        if 'transitive' in word['tags']:
            formatted_word['transitive'] = True
        if 'intransitive' in word['tags']:
            formatted_word['intransitive'] = True

    related_front, related_back = format_related(word)
    formatted_word['related_front'] = related_front
    formatted_word['related_back'] = related_back
    formatted_word['notes'] = clean_notes(word.get('notes', ''))
    formatted_word.pop('related', None)
    formatted_word.pop('_relatedWords', None)

    return formatted_word


def format_all_csv_words(words):
    result = []
    for word in words:
        result.append(format_csv_word(word))
    return result
