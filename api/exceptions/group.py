from api.exceptions import ObjectNotFoundError, ConflictError


class GroupNotFoundError(ObjectNotFoundError):

    message = 'Group not found'


class GroupDoesNotBelongToSubjectError(ConflictError):

    message = 'Group does not belong to the subject'