from api.exceptions import APIError
from common import status


class CantSerializeArrayError(APIError):

    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    CODE = 'unprocessable_entity'
    MESSAGE = 'Can\'t serialize data'


