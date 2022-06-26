import jwt
from functools import wraps
from flask import request

from jap_dev.helpers.exceptions import UnauthorizedException
from jap_dev.helpers.token import decode_token


def validate_session(func):
    @wraps(func)
    def wrapped():
        try:
            token = request.headers['Authorization'].split(" ")[1]
            decode_token(token)
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException('Expired session')
        except Exception:
            raise UnauthorizedException('Invalid session')
        return func()
    return wrapped
