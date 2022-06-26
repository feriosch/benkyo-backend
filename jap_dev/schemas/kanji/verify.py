from schema import Schema, Use, Or

kanji_exists_schema = Or(
    Schema({'v1': Use(int, error='v1 error')}),
    Schema({'kanji': Use(str, error='kanji error')}),
    Schema({'spanish': Use(str, error='spanish error')}),
    error='Schema error: Only use v1, kanji or spanish as parameter',
)
