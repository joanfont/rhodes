from api.exceptions import APIError
from common import status


class CantSerializeArrayError(APIError):

    message = 'Can\'t serialize data'
    code = 'unprocessable_entity'
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


