from functools import wraps
from flask import request, make_response, jsonify
from schema import SchemaError
from jap_dev.factories.schema_factory import SchemaFactory


def validate_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                if request.method == 'GET':
                    params = request.args.to_dict(flat=True)
                    schema_fac = SchemaFactory(schema, request.method)
                    schema_fac.load_schema().validate(params)
                    return func(params)
                elif request.method == 'POST' or request.method == 'PUT':
                    body = request.json
                    schema_fac = SchemaFactory(schema, request.method)
                    schema_fac.load_schema().validate(body)
                    return func(body)
                else:
                    print(request.method)
                    print(type(request.method))
                    raise SchemaError('Method not supported.')
            except SchemaError as error:
                return make_response(
                    jsonify({'error': error.code}), 400
                )
        return wrapped
    return decorator
