from schema import Schema, Optional, Use

clause_get_schema = Schema({
    Optional('level'): Use(str),
    Optional('filter_by'): Use(str),
    Optional('order_field'): Use(str),
    Optional('order_direction'): Use(str),
    Optional('page_size'): Use(int),
    Optional('page_number'): Use(int)
})
