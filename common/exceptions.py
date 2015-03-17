import common.status as status


# Base exception
class BaseError(Exception):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    CODE = 'generic_error'
    MESSAGE = 'Generic error'

    def __init__(self, *args, **kwargs):
        super(BaseError, self).__init__(*args)
        self.status_code = kwargs.get('status_code', self.STATUS_CODE)
        if kwargs.get('error'):
            self.error = kwargs.get('error')
        else:
            message = kwargs.get('error_message', self.MESSAGE)
            self.error = {'code': self.CODE, 'message': message}


# Validation exception
class ValidationError(BaseError):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    CODE = 'validation_error'
    MESSAGE = 'Validation error'

    def append_errors(self, errors):
        self.error.update({'errors': errors})


# Service exceptions
class ServiceError(BaseError):
    pass


class ObjectNotFoundError(ServiceError):

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    CODE = 'not_found'
    MESSAGE = 'Object not found'


class GroupNotFoundError(ObjectNotFoundError):

    MESSAGE = 'Group not found'


class UserNotFoundError(ObjectNotFoundError):

    MESSAGE = 'User not found'


class SubjectNotFoundError(ObjectNotFoundError):

    MESSAGE = 'Subject not found'


class TeacherDoesNotTeachSubjectError(ObjectNotFoundError):

    MESSAGE = 'Teacher does not teach the subject'


class StudentIsNotEnrolledToSubjectError(ObjectNotFoundError):

    MESSAGE = 'Student is not enrolled to the subject'


# API errors
class APIError(BaseError):
    pass


class NotAuthenticatedError(APIError):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    CODE = 'unauthorized'
    MESSAGE = 'You are not authorized to perform this action'


class CantSerializeArrayError(APIError):
    STATUS_CODE = status.HTTP_422_UNPROCESSABLE_ENTITY
    CODE = 'unauthorized'
    MESSAGE = 'You are not authorized to perform this action'