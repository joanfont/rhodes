class BaseError(Exception):

    message = 'Generic error'
    code = 'generic_error'
    payload = {}

    def __init__(self, message=None, code=None, payload=None):
        if message:
            self.message = message

        if code:
            self.code = code

        if payload:
            self.payload = payload

