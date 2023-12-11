from schema import Schema, Optional, Use

word_csv_get_schema = Schema({
    Optional('group'): Use(str, error='collection error'),
    Optional('usually_kana'): Use(bool, error='usually_kana error')
})
