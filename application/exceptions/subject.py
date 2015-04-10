from application.exceptions import ObjectNotFoundError


class SubjectNotFoundError(ObjectNotFoundError):

    MESSAGE = 'Subject not found'