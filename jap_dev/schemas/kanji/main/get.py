from schema import Schema, Optional, Use

kanji_get_schema = Schema({
    Optional('c1'): Use(str, error='Component 1 error'),
    Optional('c2'): Use(str, error='Component 2 error'),
    Optional('c3'): Use(str, error='Component 3 error'),
    Optional('c4'): Use(str, error='Component 4 error'),
    Optional('c5'): Use(str, error='Component 5 error'),
    Optional('c6'): Use(str, error='Component 6 error'),
    Optional('filter_by'): Use(str, error='Filter error'),
    Optional('order_field'): Use(str, error='Order field error'),
    Optional('order_direction'): Use(str, error='Order direction error'),
    Optional('page_size'): Use(int, error='Page size error'),
    Optional('page_number'): Use(int, 'Page number error')
})
