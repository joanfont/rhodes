from api.exceptions import ObjectNotFoundError


class GroupNotFoundError(ObjectNotFoundError):

    message = 'Group not found'


# TODO: fix
class GroupDoesNotBelongToSubjectError(ObjectNotFoundError):

    message = 'Group does not belong to the subject'