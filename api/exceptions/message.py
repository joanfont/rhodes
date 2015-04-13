from api.exceptions import ObjectNotFoundError


class MessageNotFoundErorr(ObjectNotFoundError):

    message = 'Message not found'