import hashlib
import hmac
import base64


def encode_password(password):
    m = hashlib.md5()
    m.update(password)
    return m.hexdigest()


def encode_auth_token(token):
    return base64.b64encode(token)


def decode_auth_token(token):
    return base64.b64decode(token)


def generate_auth_token(message, secret):

    message = bytes(message).encode('utf8')
    secret = bytes(secret).encode('utf8')

    digest = hmac.new(secret, message, digestmod=hashlib.sha256).digest()
    return digest