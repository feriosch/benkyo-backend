from schema import Schema, Or, Use, Optional, And

kanji_search_one_schema = Or(
    Schema({'kanji_id': Use(str, error='kanji id error')}),
    Schema({Optional('kanji'): And(Use(str), lambda x: len(x) == 1, error='kanji error')}),
    Schema({Optional('v1'): And(Use(int), error='V1 error')})
)
