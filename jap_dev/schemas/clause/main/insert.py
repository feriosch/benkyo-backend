from schema import Schema, Optional, Use

clause_type = {
    Optional('adjective'): Use(bool, error='type.adjective error'),
    Optional('adverb'): Use(bool, error='type.adverb error'),
    Optional('auxiliary'): Use(bool, error='type.auxiliary error'),
    Optional('conjunction'): Use(bool, error='type.conjunction error'),
    Optional('modifier'): Use(bool, error='type.modifier error'),
    Optional('noun'): Use(bool, error='type.noun error'),
    Optional('particle'): Use(bool, error='type.particle error'),
    Optional('phrase'): Use(bool, error='type.phrase error'),
    Optional('structure'): Use(bool, error='type.structure error'),
    Optional('suffix'): Use(bool, error='type.suffix error')
}

clause_tags = {
    Optional('spoken'): Use(bool, error='tags.spoken error'),
    Optional('written'): Use(bool, error='tags.written error'),
    Optional('formal'): Use(bool, error='tags.formal error'),
    Optional('colloquial'): Use(bool, error='tags.colloquial error'),
    Optional('interrogative'): Use(bool, error='tags.interrogative error')
}

clause_example = {
    'sentence': Use(str, error='example.sentence error'),
    'translation': Use(str, error='example.translation error')
}

clause_formation = {
    'rule': Use(str, error='formation.rule error'),
    'examples': Schema([clause_example])
}

clause_section = {
    'explanation': Use(str, error='section.explanation error'),
    Optional('examples'): Schema([clause_example])
}

clause_related = {
    'title': Use(str, error='related.title error'),
    Optional('hiragana'): Use(str, error='related.hiragana error'),
    Optional('reference'): Use(str, error='related.reference error'),
    'sections': Schema([clause_section])
}

clause_insert_schema = Schema({
    'title': Use(str, error='title error'),
    Optional('hiragana'): Use(str, error='hiragana error'),
    'translation': Use(str, error='translation error'),
    'level': Use(str, error='level error'),
    'clause_type': Schema(clause_type),
    Optional('tags'): Schema(clause_tags),
    'definition': Use(str, error='definition error'),
    'keys': Schema([clause_example]),
    'formations': Schema([clause_formation]),
    Optional('examples'): Schema([clause_example]),
    'notes': Schema([clause_section]),
    Optional('related'): Schema([clause_related])
})
