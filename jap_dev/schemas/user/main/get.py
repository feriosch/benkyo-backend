from schema import Schema, Optional, Use

user_get_schema = Schema({
    Optional('test'): Use(str, error='Parameter test invalid'),
})
