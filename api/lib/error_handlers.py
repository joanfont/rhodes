from flask import jsonify
from api.exceptions import ObjectNotFoundError, ForbiddenActionError, ConflictError
from api.exceptions.auth import NotAuthenticatedError
from api.exceptions.response import CantSerializeArrayError
from application.exceptions import ValidationError as ApplicationValidationError
from api.exceptions.validation import ValidationError as APIValidationError


# workaround, we translate an Application ValidationError without stauts_code
# into an API Validation Error with status_code (400 Bad Request)
def app_validation_error_handler(error):
    errors = error.to_dict()
    api_validation_error = APIValidationError(payload=errors)
    data = api_validation_error.to_dict()

    response = jsonify(data)
    response.status_code = api_validation_error.status_code

    return response


def api_error_handler(error):

    data = error.to_dict()

    response = jsonify(data)
    response.status_code = error.status_code

    return response


handlers = {
    # generic errors
    [ObjectNotFoundError, ForbiddenActionError, ConflictError]: api_error_handler,

    # auth errors
    [NotAuthenticatedError]: api_error_handler,
    [CantSerializeArrayError]: api_error_handler,

    # special case for validation errors
    [ApplicationValidationError]: app_validation_error_handler

}