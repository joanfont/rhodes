import hashlib
import hmac
from common.helper import Helper


def encode_password(password):
    return Helper.md5(password)


def encode_auth_token(token):
    return Helper.b64_encode(token)


def decode_auth_token(token):
    return Helper.b64_decode(token)


def generate_auth_token(message, secret):

    message = bytes(message).encode('utf8')
    secret = bytes(secret).encode('utf8')

    digest = hmac.new(secret, message, digestmod=hashlib.sha256).digest()
    return digest