import jwt

from jap_dev.helpers.exceptions import UnauthorizedException
from jap_dev.helpers.token import decode_token


def validate_session(req):
    try:
        token = req.headers['Authorization'].split(" ")[1]
        decode_token(token)
    except jwt.ExpiredSignatureError:
        raise UnauthorizedException("Expired session")
    except Exception:
        raise UnauthorizedException("Invalid session")
    return True
