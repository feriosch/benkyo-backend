from importlib import import_module


class SchemaFactory:
    # Factory to get the correct schema according to the method of request. In case it doesnt finds a
    # specific implementation it will use a generic schema defined by the schema name without suffix
    def __init__(self, schema, method):
        self.schema = schema
        self.method = method

    def load_schema(self):
        schema_module = import_module('.helpers.schemas', 'jap_dev')
        try:
            schema = getattr(schema_module, self.schema + '_' + self.method.lower())
        except AttributeError:
            schema = getattr(schema_module, self.schema)
        return schema
