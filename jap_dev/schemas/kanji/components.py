from schema import Schema, Optional, Use, And

kanji_components_schema = Schema({
    Optional('starting'): Use(str, error='starting error'),
    Optional('limit'): And(Use(int), lambda x: 0 < x < 50, error='limit error'),
})
