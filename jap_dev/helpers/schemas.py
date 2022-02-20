from schema import Schema, Use, And, Optional, Or


test_schema = Schema({
    'test': Use(str,
                error='Parameter test invalid'),
    'test_int': Use(int,
                    error='Parameter test_int invalid')
})

user_schema = Schema({
    Optional('test'): Use(str, error='Parameter test invalid'),
})

user_schema_post = Schema({
    'username': Use(str, error='Username parameter invalid'),
    'password': Use(str, error='Password parameter invalid'),
    'type': And(Use(str),
                lambda x: x in ['admin', 'regular'],
                error='Type parameter invalid'),
})

login_schema = Schema({
    'username': Use(str, error='username parameter invalid'),
    'password': Use(str, error='password parameter invalid')
})

group_collections_schema = Schema({
    Optional('group'): Use(str, error='group parameter error'),
    Optional('name'): Use(str, error='name parameter error')
})

group_collections_schema_post = Schema({
    'printing_name': Use(str, error='printing_name error'),
    'collection_name': Use(str, error='collection_name error'),
    'group': Use(str, error='group error')
})

word_type_schema = Schema({
    Optional('noun'): And(Use(int), lambda x: 0 <= x <= 9, error='type.noun error'),
    Optional('suru_verb'): And(Use(int), lambda x: 0 <= x <= 9, error='type.suru_verb error'),
    Optional('no_adjective'): And(Use(int), lambda x: 0 <= x <= 9, error='type.no_adjective error'),
    Optional('na_adjective'): And(Use(int), lambda x: 0 <= x <= 9, error='type.na_adjective error'),
    Optional('i_adjective'): And(Use(int), lambda x: 0 <= x <= 9, error='type.i_adjective error'),
    Optional('adverb'): And(Use(int), lambda x: 0 <= x <= 9, error='type.adverb error'),
    Optional('verb'): And(Use(int), lambda x: 0 <= x <= 9, error='type.verb error'),
    Optional('adjectival_noun'): And(Use(int), lambda x: 0 <= x <= 9, error='type.adjectival_noun error'),
    Optional('adverbial_noun'): And(Use(int), lambda x: 0 <= x <= 9, error='type.adverbial_noun error'),
    Optional('counter'): And(Use(int), lambda x: 0 <= x <= 9, error='type.counter error'),
})

word_tags_schema = Schema({
    Optional('ateji'): Use(bool, error='tags.ateji error'),
    Optional('common'): Use(bool, error='tags.common error'),
    Optional('expression'): Use(bool, error='tags.expression error'),
    Optional('honorific'): Use(bool, error='tags.honorific error'),
    Optional('humble'): Use(bool, error='tags.humble error'),
    Optional('intransitive'): Use(bool, error='tags.intransitive error'),
    Optional('jlpt_n1'): Use(bool, error='tags.jlpt_n1 error'),
    Optional('joyogai'): Use(bool, error='tags.joyogai error'),
    Optional('onomatopeic'): Use(bool, error='tags.onomatopeic error'),
    Optional('transitive'): Use(bool, error='tags.transitive error'),
    Optional('usually_kana'): Use(bool, error='tags.usually_kana error'),
})

word_schema = Schema({
    Optional('from'): Use(str),
    Optional('filter_by'): Use(str),
    Optional('order_field'): Use(str),
    Optional('order_direction'): Use(str),
    Optional('page_size'): Use(int),
    Optional('page_number'): Use(int)
})

word_schema_post = Schema({
    'word': Use(str, error='word error'),
    'spanish': Use(str, error='spanish error'),
    'from': And(Use(str), lambda x: x != 'all', error='from (collection) error'),
    Optional('hiragana'): Use(str, error='hiragana error'),
    Optional('level'): And(Use(int), lambda x: 0 <= x <= 5, error='level error'),
    Optional('word_type'): word_type_schema,
    Optional('tags'): word_tags_schema,
    Optional('sentences'): Schema([{
        'sentence': Use(str, error='sentences.sentence error'),
        'translation': Use(str, error='sentences.translation error')
    }]),
    Optional('notes'): Use(str, error='notes error')
})

word_schema_put = Schema({
    'word_id': Use(str, error='id error (required)'),
    Optional('from'): Use(str, error='collection error'),
    Optional('spanish'): Use(str, error='spanish error'),
    Optional('hiragana'): Use(str, error='hiragana error'),
    Optional('word_type'): word_type_schema,
    Optional('tags'): word_tags_schema,
    Optional('sentences'): Schema([{
        'sentence': Use(str, error='sentences.sentence error'),
        'translation': Use(str, error='sentences.translation error')
    }]),
    Optional('notes'): Use(str, error='notes error')
})

word_schema_delete = Schema({
    'word_id': Use(str, error='id error (required)')
})

search_word_schema = Schema({
    'word': Use(str, error='Word Is Missing')
})

search_one_word_schema = Or(
    Schema({'word': Use(str, error='Word Is Missing')}),
    Schema({'word_id': Use(str, error='Id Is Missing')}),
    Schema({Optional('from'): Use(str, error='Collection error')}),
    error='Schema error: Only use word, id or from collection (optional) as parameter',
)

update_word_level_schema = Schema({
    'word_id': Use(str, error='Id is missing'),
    'success': Use(int, error='Success is missing')
})

kanji_schema = Schema({
    Optional('c1'): Use(str, error='Component 1 error'),
    Optional('c2'): Use(str, error='Component 2 error'),
    Optional('c3'): Use(str, error='Component 3 error'),
    Optional('c4'): Use(str, error='Component 4 error'),
    Optional('c5'): Use(str, error='Component 5 error'),
    Optional('c6'): Use(str, error='Component 6 error'),
    Optional('filter_by'): Use(str, error='Filter error'),
    Optional('order_field'): Use(str, error='Order field error'),
    Optional('order_direction'): Use(str, error='Order direction error'),
    Optional('page_size'): Use(int, error='Page size error'),
    Optional('page_number'): Use(int, 'Page number error')
})

kanji_schema_post = Schema({
    'v1': Use(int, error='v1 error'),
    Optional('v2'): Use(int, error='v2 error'),
    'kanji': Use(str, error='kanji error'),
    Optional('on'): Use(str, error='on error'),
    Optional('kun'): Use(str, error='kun error'),
    'spanish': Use(str, 'spanish error'),
    Optional('components'): Schema([
        Use(str, error='component error')
    ]),
    Optional('story'): Use(str, error='story error'),
})

kanji_schema_put = Schema({
    'kanji_id': Use(str, error='id is missing'),
    'v1': Use(int, error='v1 error'),
    Optional('v2'): Use(int, error='v2 error'),
    'kanji': Use(str, error='kanji error'),
    Optional('on'): Use(str, error='on error'),
    Optional('kun'): Use(str, error='kun error'),
    'spanish': Use(str, 'spanish error'),
    Optional('components'): Schema([
        Use(str, error='component error')
    ]),
    Optional('story'): Use(str, error='story error'),
})

exists_kanji_schema = Or(
    Schema({'v1': Use(int, error='v1 error')}),
    Schema({'kanji': Use(str, error='kanji error')}),
    Schema({'spanish': Use(str, error='spanish error')}),
    error='Schema error: Only use v1, kanji or spanish as parameter',
)

kanji_components_schema = Schema({
    Optional('starting'): Use(str, error='starting error'),
    Optional('limit'): And(Use(int), lambda x: 0 < x < 50, error='limit error'),
})

search_one_kanji_schema = Or(
    Schema({'kanji_id': Use(str, error='kanji id error')}),
    Schema({Optional('kanji'): And(Use(str), lambda x: len(x) == 1, error='kanji error')}),
)
