from schema import Schema, Optional, Use, And

kanji_components_schema = Schema({
    Optional('prefix'): Use(str, error='prefix error'),
    Optional('page_size'): And(Use(int), lambda x: x > 0, error='Page size error'),
    Optional('page_number'): And(Use(int), lambda x: x > 0, error='Page number error'),
})
