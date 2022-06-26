from schema import Schema, Use, And

user_insert_schema = Schema({
    'username': Use(str, error='Username parameter invalid'),
    'password': Use(str, error='Password parameter invalid'),
    'type': And(Use(str),
                lambda x: x in ['admin', 'regular'],
                error='Type parameter invalid'),
})
