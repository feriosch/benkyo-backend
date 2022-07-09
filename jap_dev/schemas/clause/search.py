from schema import Schema, Use

search_clause_schema = Schema({'clause_id': Use(str, error='clause id error')})
