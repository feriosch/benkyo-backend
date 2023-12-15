from schema import Schema, Optional, Use, And

word_type_insert_schema = Schema({
    Optional('noun'): And(Use(int), lambda x: 0 < x <= 9, error='type.noun error'),
    Optional('suru'): And(Use(int), lambda x: 0 < x <= 9, error='type.suru error'),
    Optional('no_adj'): And(Use(int), lambda x: 0 < x <= 9, error='type.no_adj error'),
    Optional('na_adj'): And(Use(int), lambda x: 0 < x <= 9, error='type.na_adj error'),
    Optional('i_adj'): And(Use(int), lambda x: 0 < x <= 9, error='type.i_adj error'),
    Optional('adv'): And(Use(int), lambda x: 0 < x <= 9, error='type.adv error'),
    Optional('verb'): And(Use(int), lambda x: 0 < x <= 9, error='type.verb error'),
    Optional('adj_noun'): And(Use(int), lambda x: 0 < x <= 9, error='type.adj_noun error'),
    Optional('adv_noun'): And(Use(int), lambda x: 0 < x <= 9, error='type.adv_noun error'),
    Optional('counter'): And(Use(int), lambda x: 0 < x <= 9, error='type.counter error'),
})

word_insert_schema = Schema({
    'word': Use(str, error='word error'),
    'spanish': Use(str, error='spanish error'),
    'group': And(Use(str), lambda x: x != 'all', error='from (collection) error'),
    Optional('hiragana'): Use(str, error='hiragana error'),
    Optional('level'): And(Use(int), lambda x: 0 <= x <= 5, error='level error'),
    Optional('word_type'): word_type_insert_schema,
    Optional('tags'): Schema([Use(str, error='tag error')]),
    Optional('sentences'): Schema([{
        'sentence': Use(str, error='sentences.sentence error'),
        'translation': Use(str, error='sentences.translation error')
    }]),
    Optional('notes'): Use(str, error='notes error')
})
