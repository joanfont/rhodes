from common import status
from common.exceptions import BaseError


class ServiceError(BaseError):
    pass


class ValidationError(BaseError):
    pass


class ObjectNotFoundError(ServiceError):

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    CODE = 'not_found'
    MESSAGE = 'Object not found'
