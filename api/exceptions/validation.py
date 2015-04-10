from api.exceptions import APIError
from common import status


class InvalidParameterError(APIError):

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    CODE = 'invalid_parameter'
    MESSAGE = 'A required parameter was not provided'