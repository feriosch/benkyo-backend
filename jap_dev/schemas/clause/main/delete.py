from schema import Schema, Use

clause_delete_schema = Schema({
    'clause_id': Use(str, error='id error (required)')
})
