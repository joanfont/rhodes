from application.exceptions import ObjectNotFoundError


class GroupNotFoundError(ObjectNotFoundError):

    MESSAGE = 'Group not found'


# TODO: fix
class GroupDoesNotBelongToSubjectError(ObjectNotFoundError):

    MESSAGE = 'Group does not belong to the subject'