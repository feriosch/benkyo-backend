from schema import Schema, Optional, Use

kanji_insert_schema = Schema({
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
