from api.exceptions import APIError, ForbiddenActionError
from common import status


class NotAuthenticatedError(APIError):

    message = 'You are not authorized to perform this action'
    code = 'unauthorized'
    status_code = status.HTTP_401_UNAUTHORIZED


class NotEnoughPermissionError(ForbiddenActionError):

    message = 'You don\'t have enough permissions to perform this action'
