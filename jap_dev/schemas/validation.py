from functools import wraps
from schema import SchemaError
from flask import request, jsonify, make_response


def get_params():
    try:
        if request.method == 'GET' or request.method == 'DELETE':
            params = request.args.to_dict()
        elif request.method == 'POST' or request.method == 'PUT':
            params = request.json
        else:
            raise SchemaError('Method not supported.')
    except SchemaError as error:
        return make_response(
            jsonify({'error': error.code}), 400
        )
    return params


def validate_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            try:
                params = get_params()
                schema.validate(params)
                return func(params)
            except SchemaError as error:
                return make_response(
                    jsonify({'error': error.code}), 400
                )
        return wrapped
    return decorator
