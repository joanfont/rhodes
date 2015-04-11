from common import status
from common.exceptions import BaseError


class ServiceError(BaseError):
    pass


class ValidationError(BaseError):
    pass
