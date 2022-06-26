from schema import Schema, Optional, Use, And

word_type_insert_schema = Schema({
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

word_tags_insert_schema = Schema({
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

word_insert_schema = Schema({
    'word': Use(str, error='word error'),
    'spanish': Use(str, error='spanish error'),
    'from': And(Use(str), lambda x: x != 'all', error='from (collection) error'),
    Optional('hiragana'): Use(str, error='hiragana error'),
    Optional('level'): And(Use(int), lambda x: 0 <= x <= 5, error='level error'),
    Optional('word_type'): word_type_insert_schema,
    Optional('tags'): word_tags_insert_schema,
    Optional('sentences'): Schema([{
        'sentence': Use(str, error='sentences.sentence error'),
        'translation': Use(str, error='sentences.translation error')
    }]),
    Optional('notes'): Use(str, error='notes error')
})
