from schema import Schema, Optional, Use

collection_get_schema = Schema({
    Optional('group'): Use(str, error='group parameter error'),
    Optional('name'): Use(str, error='name parameter error')
})
