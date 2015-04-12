from common.exceptions import BaseError


class MyValueError(BaseError):

    message = 'Internal value error'
    code = 'internal_value_error'
    errors = {}

    def __init__(self, message=None, code=None, payload=None, errors=None):
        super(MyValueError, self).__init__(message, code, payload)

        self.errors = errors

    def get_errors(self):
        return self.errors


class ValidationError(BaseError):

    message = 'Validation error'
    code = 'validation_error'


class ServiceError(BaseError):
    pass



