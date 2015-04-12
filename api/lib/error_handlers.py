from flask import jsonify
from application.exceptions import ValidationError as ApplicationValidationError
from api.exceptions.validation import ValidationError as APIValidationError


# workaround
def app_validation_error_handler(error):

    errors = error.to_dict()
    api_validation_error = APIValidationError(payload=errors)
    data = api_validation_error.to_dict()

    response = jsonify(data)
    response.status_code = api_validation_error.status_code

    return response


handlers = {
    ApplicationValidationError: app_validation_error_handler
}