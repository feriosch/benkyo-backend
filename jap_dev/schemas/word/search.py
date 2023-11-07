from schema import Schema, Or, Use, Optional

search_word_schema = Or(
    Schema({'word': Use(str, error='Word Is Missing')}),
    Schema({'word_id': Use(str, error='Id Is Missing')}),
    Schema({Optional('group'): Use(str, error='Collection error')}),
    error='Schema error: Only use word, id or from collection (optional) as parameter',
)
