from common.exceptions import BaseError
from common import status


class APIError(BaseError):

    message = 'Internal Server Error'
    code = 'internal_server_error'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message=None, code=None, status_code=None, payload=None):
        super(APIError, self).__init__(message, code, payload)

        if status_code:
            self.status_code = status_code


class ObjectNotFoundError(APIError):

    message = 'Object not found'
    code = 'not_found'
    status_code = status.HTTP_404_NOT_FOUND


class ForbiddenActionError(APIError):

    message = 'Forbidden'
    code = 'forbidden'
    status_code = status.HTTP_403_FORBIDDEN


class ConflictError(APIError):

    message = 'Conflict'
    code = 'conflict'
    status_code = status.HTTP_409_CONFLICT