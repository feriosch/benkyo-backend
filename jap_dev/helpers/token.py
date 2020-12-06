import jwt
from dotenv import load_dotenv
import os

load_dotenv()


def generate_token(claims):
    return jwt.encode(claims, os.getenv('TOKEN_PASS'), algorithm='HS256')


def decode_token(token):
    return jwt.decode(token, os.getenv('TOKEN_PASS'), algorithms='HS256')
