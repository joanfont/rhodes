from api.exceptions import ObjectNotFoundError


class SubjectNotFoundError(ObjectNotFoundError):

    message = 'Subject not found'