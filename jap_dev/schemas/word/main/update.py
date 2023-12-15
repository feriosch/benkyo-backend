from schema import Schema, Optional, Use

from jap_dev.schemas.word.main.insert import word_type_insert_schema

word_update_schema = Schema({
    'word_id': Use(str, error='id error (required)'),
    Optional('group'): Use(str, error='collection error'),
    Optional('spanish'): Use(str, error='spanish error'),
    Optional('hiragana'): Use(str, error='hiragana error'),
    Optional('word_type'): word_type_insert_schema,
    Optional('tags'): Schema([Use(str, error='tag error')]),
    Optional('sentences'): Schema([{
        'sentence': Use(str, error='sentences.sentence error'),
        'translation': Use(str, error='sentences.translation error')
    }]),
    Optional('notes'): Use(str, error='notes error')
})
