from common.exceptions import BaseError
from common import status


class APIError(BaseError):

    message = 'Internal Server Error'
    code = 'internal_server_error'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = {}

    def __init__(self, message, code=None, status_code=None, payload=None):

        if message:
            self.message = message

        if code:
            self.code = code

        if status_code:
            self.status_code = status_code

        if payload:
            error = dict(payload)
        else:
            error = {'code': self.code, 'message': self.message}

        self.error = error


class ObjectNotFoundError(BaseError):

    message = 'Object not found'
    code = 'not_found'
    status_code = status.HTTP_404_NOT_FOUND