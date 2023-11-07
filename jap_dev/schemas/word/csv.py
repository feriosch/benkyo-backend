from schema import Schema, Optional, Use

word_csv_get_schema = Schema({
    Optional('group'): Use(str, error='Collection error')
})
