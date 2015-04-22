import json


class BaseError(Exception):

    message = 'Generic error'
    code = 'generic_error'
    payload = {}

    def __init__(self, message=None, code=None, payload=None):

        if message:
            self.message = message

        if code:
            self.code = code

        if isinstance(payload, dict):
            self.payload = payload

    def to_dict(self):
        data = self.payload
        data.update({'code': self.code, 'message': self.message})
        return data

    def to_string(self):
        args = {
            'code': self.code,
            'message': self.message,
            'payload': json.dumps(self.payload)
        }
        return '\nCODE: {code}\nMESSAGE: {message}\nPAYLOAD: {payload}'.format(**args)

