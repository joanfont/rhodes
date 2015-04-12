from api.exceptions import APIError
from common import status


class ValidationError(APIError):

    message = 'Validation error'
    code = 'validation_error'
    status_code = status.HTTP_400_BAD_REQUEST