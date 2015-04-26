from api.exceptions import ObjectNotFoundError, ConflictError


class MessageNotFoundErorr(ObjectNotFoundError):

    message = 'Message not found'


class MessageKindIsNotSubjectMessageErrror(ConflictError):

    message = 'Message does not belong to any subject'


class MessageDoesNotBelongToSubjectError(ConflictError):

    message = 'Message does not belong to subject'


class MessageKindIsNotGroupMessageErrror(ConflictError):

    message = 'Message does not belong to any group'


class MessageDoesNotBelongToGroupError(ConflictError):

    message = 'Message does not belong to group'


class ConversationDoesNotExistsBetweenUsersError(ConflictError):

    message = 'Conversation does not exists between users'