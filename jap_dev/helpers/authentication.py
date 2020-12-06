import jwt
from functools import wraps
from flask import request

from jap_dev.helpers.exceptions import UnauthorizedException
from jap_dev.helpers.token import decode_token


def authenticate_jwt():
    """
    Authenticaion decorators, check for the existance of a jwt in the
    authentication header and if present continues with the request and add
    the user info into the params.
    """
    def decorator(func):
        @wraps(func)
        def wrapped(params):
            try:
                auth_jwt = request.headers['Authorization']
                info = decode_token(auth_jwt)
            except jwt.ExpiredSignatureError:
                raise UnauthorizedException("Expired JWT")
            except Exception:
                raise UnauthorizedException("Missing JWT")

            params.update(info)
            return func(params)
        return wrapped
    return decorator
