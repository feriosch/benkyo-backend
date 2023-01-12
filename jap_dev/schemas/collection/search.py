from schema import Schema, Use

search_collection_schema = Schema({'name': Use(str)})
