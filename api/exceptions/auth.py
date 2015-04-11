from api.exceptions import APIError
from common import status


class NotAuthenticatedError(APIError):

    message = 'You are not authorized to perform this action'
    code = 'unauthorized'
    status_code = status.HTTP_401_UNAUTHORIZED


class NotEnoughPermissionError(APIError):

    message = 'You don\'t have enough permissions to perform this action'
    code = 'forbidden'
    status_code = status.HTTP_403_FORBIDDEN
