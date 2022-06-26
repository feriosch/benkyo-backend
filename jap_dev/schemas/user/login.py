from schema import Schema, Use

user_login_schema = Schema({
    'username': Use(str, error='username parameter invalid'),
    'password': Use(str, error='password parameter invalid')
})
