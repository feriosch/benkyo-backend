from schema import Schema, Optional, Use

word_csv_get_schema = Schema({
    Optional('from'): Use(str, error='Collection error')
})
