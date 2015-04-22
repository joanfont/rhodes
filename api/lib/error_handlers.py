from flask import jsonify
from api.exceptions import ObjectNotFoundError, ForbiddenActionError, ConflictError
from api.exceptions.auth import NotAuthenticatedError
from api.exceptions.response import CantSerializeArrayError
from application.exceptions import ValidationError as ApplicationValidationError
from api.exceptions.validation import ValidationError as APIValidationError

from api.app import app


class BaseBehaviour(object):

    def __call__(self, error):
        raise NotImplementedError()

    @staticmethod
    def get_error_repr(error):
        return error.to_string()


class FileLoggingBehaviour(BaseBehaviour):

    def __call__(self, error):
        error_repr = self.get_error_repr(error)
        app.logger.error(error_repr)


class SMTPLoggingBehaviour(BaseBehaviour):

    def __call__(self, error):
        pass


class BaseErrorHandler(object):

    def __init__(self, behaviours=[]):
        self.behaviours = behaviours

    def __call__(self, error):

        for behaviour_class in self.behaviours:
            behaviour_instance = behaviour_class()
            behaviour_instance(error)


class APIErrorHandler(BaseErrorHandler):

    def __init__(self):
        super(APIErrorHandler, self).__init__()
        self.behaviours.append(FileLoggingBehaviour)

    def __call__(self, error):
        data = error.to_dict()

        response = jsonify(data)
        response.status_code = error.status_code

        super(APIErrorHandler, self).__call__(error)

        return response


class AppValidationErrorHandler(BaseErrorHandler):

    def __init__(self):
        super(AppValidationErrorHandler, self).__init__()
        self.behaviours.append(FileLoggingBehaviour)

    def __call__(self, error):
        errors = error.to_dict()
        api_validation_error = APIValidationError(payload=errors)
        data = api_validation_error.to_dict()

        response = jsonify(data)
        response.status_code = api_validation_error.status_code

        super(AppValidationErrorHandler).__call__(error)

        return response


handlers = {

    # generic errors
    (ObjectNotFoundError, ForbiddenActionError, ConflictError): APIErrorHandler(),

    # auth errors
    NotAuthenticatedError: APIErrorHandler(),

    # response errors
    CantSerializeArrayError: APIErrorHandler(),

    # api validation errors
    APIValidationError: APIErrorHandler(),

    # special case for application validation errors
    ApplicationValidationError: AppValidationErrorHandler()

}