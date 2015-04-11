from common.exceptions import BaseError


class MyValueError(BaseError):

    message = 'Internal value error'
    code = 'internal_value_error'


class ValidationError(BaseError):

    message = 'Validation error'
    code = 'validation_error'


class ServiceError(BaseError):
    pass



