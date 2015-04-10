from api.exceptions import APIError
from common import status


class NotAuthenticatedError(APIError):

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    CODE = 'unauthorized'
    MESSAGE = 'You are not authorized to perform this action'


class NotEnoughPermissionError(APIError):

    STATUS_CODE = status.HTTP_403_FORBIDDEN
    CODE = 'forbidden'
    MESSAGE = 'You don\'t have enough permissions to perform this action'