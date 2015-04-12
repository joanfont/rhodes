from flask import jsonify
from application.exceptions import ValidationError as ApplicationValidationError
from api.exceptions.validation import ValidationError as APIValidationError


def api_validation_error_handler(error):
    data = error.to_dict()

    response = jsonify(data)
    response.status_code = error.status_code

    return response


def app_validation_error_handler(error):
    raise APIValidationError(payload=error.payload)


handlers = {
    ApplicationValidationError: app_validation_error_handler,
    APIValidationError: api_validation_error_handler

}