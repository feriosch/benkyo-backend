from schema import Schema, Use

collection_insert_schema = Schema({
    'printing_name': Use(str, error='printing_name error'),
    'collection_name': Use(str, error='collection_name error'),
    'group': Use(str, error='group error')
})
