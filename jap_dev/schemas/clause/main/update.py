from schema import Schema, Optional, Use

import jap_dev.schemas.clause.main.insert as insert_schemas

clause_update_schema = Schema({
    'clause_id': Use(str, error='id error (required)'),
    Optional('hiragana'): Use(str, error='hiragana error'),
    Optional('translation'): Use(str, error='translation error'),
    Optional('level'): Use(str, error='level error'),
    Optional('clause_type'): Schema(insert_schemas.clause_type),
    Optional('tags'): Schema(insert_schemas.clause_tags),
    Optional('definition'): Use(str, error='definition error'),
    Optional('keys'): Schema([insert_schemas.clause_example]),
    Optional('formations'): Schema([insert_schemas.clause_formation]),
    Optional('examples'): Schema([insert_schemas.clause_example]),
    Optional('notes'): Schema([insert_schemas.clause_section]),
    Optional('related'): Schema([insert_schemas.clause_related])
})
