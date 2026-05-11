import re


TYPE_PREFIXES = {'synonym': '=', 'antonym': '✕', 'related': '~'}

NUANCE_CSS_CLASS = {
    'formal': 'formal',
    'casual': 'casual',
    'literary': 'literary',
    'technical': 'technical',
    'archaic': 'archaic',
    'spoken': 'spoken',
    'polite': 'formal',
    'written': 'literary',
    'slang': 'casual',
}

DEFAULT_TYPE_CLASS = {
    'synonym': 'syn',
    'antonym': 'ant',
    'related': 'rel-default',
}

REL_NOTE_PATTERNS = [
    r'rel:\s*[^;]+(?:;|$)',
    r'sinonimo:\s*[^;]+(?:;|$)',
    r'antonimo:\s*[^;]+(?:;|$)',
]


def format_related(word):
    related = word.get('related', [])
    lookup = word.get('_relatedWords', [])
    if not related:
        return ''

    word_map = {}
    for w in lookup:
        oid = str(w['_id'])
        word_map[oid] = w.get('word') or w.get('hiragana', '?')

    pills = []
    for rel in related:
        word_id = str(rel['wordId'])
        rel_word = word_map.get(word_id, '')
        if not rel_word:
            continue

        rel_type = rel.get('type', 'related')
        nuance_tags = rel.get('tags', [])
        prefix = TYPE_PREFIXES.get(rel_type, '~')

        if nuance_tags:
            css_class = NUANCE_CSS_CLASS.get(nuance_tags[0], DEFAULT_TYPE_CLASS.get(rel_type, 'rel-default'))
        else:
            css_class = DEFAULT_TYPE_CLASS.get(rel_type, 'rel-default')

        pills.append(f'<span class="rel-pill {css_class}">{prefix} {rel_word}</span>')

    return ' '.join(pills)


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

    formatted_word['related_html'] = format_related(word)
    formatted_word['notes'] = clean_notes(word.get('notes', ''))
    formatted_word.pop('related', None)
    formatted_word.pop('_relatedWords', None)

    return formatted_word


def format_all_csv_words(words):
    result = []
    for word in words:
        result.append(format_csv_word(word))
    return result
