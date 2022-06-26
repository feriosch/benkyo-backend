from schema import Schema, Use

word_delete_schema = Schema({
    'word_id': Use(str, error='id error (required)')
})
