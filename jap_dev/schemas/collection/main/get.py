from schema import Schema, Optional, Use

collection_get_schema = Schema({
    Optional('group'): Use(str),
    Optional('filter'): Use(str),
    Optional('page_size'): Use(int),
    Optional('page_number'): Use(int)
})
