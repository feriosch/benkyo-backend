from schema import Schema, Optional, Use

word_csv_get_schema = Schema({
    Optional('group'): Use(str),
    Optional('tag_1'): Use(str),
    Optional('tag_2'): Use(str),
    Optional('tag_3'): Use(str),
    Optional('usually_kana'): Use(bool)
})

jlpt_word_csv_get_schema = Schema({
    Optional('usually_kana'): Use(bool)
})
