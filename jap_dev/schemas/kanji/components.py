from schema import Schema, Optional, Use, And

kanji_components_schema = Schema({
    Optional('prefix'): Use(str, error='prefix error'),
    Optional('page_size'): And(Use(int), lambda x: x > 0, error='Page size error'),
    Optional('page_number'): And(Use(int), lambda x: x > 0, error='Page number error'),
})

kanji_irregular_component_insert_schema = Schema({
    'component': Use(str, error='Component (title) error'),
    'radicals': [Use(str, error='Radicals error')],
})
