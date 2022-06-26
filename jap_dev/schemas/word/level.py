from schema import Schema, Use

word_level_update_schema = Schema({
    'word_id': Use(str, error='Id is missing'),
    'success': Use(int, error='Success is missing')
})
